import html2text

from message_schema import Updater
from plugins.systems import Systems
from plugins.config import cfg
from plugins.helper import send_message, edit_message
from plugins.pg.query import generate_search_query


async def hello_message(m: Updater,
                        systems: Systems):
    """
    Приветственное сообщение с просьбой указать навык
    :param systems: Объект с вспомогательными классами(для доступа к базам и локальному кэшу)
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    if m.message:
        await systems.local_cache.clean(m.message.chat.id)
    else:
        await systems.local_cache.clean(m.callback_query.message.chat.id)

    text = "💥 Приветствую, я найду для тебя работу. Введите свой ключевой навык❗"
    await send_message(cfg.app.hosts.tlg.send_message,
                       m.message.chat.id,
                       text,
                       remove_keyboard=True)
    return 1


async def analyze_text_and_give_vacancy(m: Updater,
                                        systems: Systems):
    """
    :param systems: Объект с вспомогательными классами(для доступа к базам и локальному кэшу)
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    # отлавливаем chat_id
    if m.message:
        chat_id = m.message.chat.id
        message_id = m.message.message_id
        text = m.message.text
    elif m.callback_query:
        chat_id = m.callback_query.message.chat.id
        message_id = m.callback_query.message.message_id
        text = m.callback_query.data
    else:
        chat_id = None
        message_id = None
        text = None
        # Подразумевается что пользователь уже вбил критерий поиска

    if await systems.local_cache.check(chat_id):

        if text == "Да":
            await systems.local_cache.next_step(chat_id)

            most_sim_vacancy_content = await systems.local_cache.give_cache(chat_id)
            if most_sim_vacancy_content:

                # TODO обратить внимание на форматирование

                # todo сделать датакласс
                inline_keyboard = [
                    [
                        {
                            "text": "Да",
                            "callback_data": "Да"
                        },
                        {
                            "text": "Нет",
                            "callback_data": "Нет"

                        }
                    ]
                ]
                # todo преобразовывать из html в text на уровне загрузки данных в базу
                await edit_message(url=cfg.app.hosts.tlg.edit_message,
                                   text=html2text.html2text(most_sim_vacancy_content['header']),
                                   message_id=message_id,
                                   chat_id=chat_id,
                                   inline_keyboard=inline_keyboard)

                return 1
            else:
                text = '🤓 К сожалению, вакансий больше нет❗️'
                await send_message(cfg.app.hosts.tlg.send_message,
                                   chat_id,
                                   text,
                                   remove_keyboard=True)
                return 0
        else:
            text = '💥 Пока, возвращайся еще❗️'
            await send_message(cfg.app.hosts.tlg.send_message,
                               chat_id,
                               text,
                               remove_keyboard=True)
            return 0

    else:
        # возвращат id вакансии
        # запрос к базе данный
        # TODO нет нормализации

        query = generate_search_query(text=text)

        ready_content = []
        columns = ["id", "title", "footer", "header",
                   "requirements", "duties", "conditions",
                   "date", "locality", "region", "company"]
        for row in await systems.pg.fetch(query):
            reconstruction: dict = {v: str(row[v]) for v in columns}
            ready_content.append(reconstruction)
        step = 0
        await systems.local_cache.caching(chat_id,
                                          step=step,
                                          arr=ready_content)
        # первый раз отсылаем сообщение
        if len(ready_content) > 0:
            # inline_buttons = ['Да', 'Нет']
            # inline_keyboard = [[{"text": text, "callback_data": "A1"} for text in inline_buttons]]
            inline_keyboard = [
                [
                    {
                        "text": "Да",
                        "callback_data": "Да"
                    },
                    {
                        "text": "Нет",
                        "callback_data": "Нет"

                    }
                ]
            ]
            await send_message(cfg.app.hosts.tlg.send_message,
                               chat_id,
                               html2text.html2text(ready_content[step]['header']),
                               inline_keyboard=inline_keyboard)
            return 1
        else:
            text = '🤓 К сожалению, я не нашел вакансии:(️'
            await send_message(cfg.app.hosts.tlg.send_message,
                               chat_id,
                               text,
                               remove_keyboard=True)
            return 0


async def goodbye_message(m: Updater):
    text = '💥 Пока, возвращайся еще❗️'
    await send_message(cfg.app.hosts.tlg.send_message,
                       m.message.chat.id,
                       text,
                       remove_keyboard=True)
    return 0
