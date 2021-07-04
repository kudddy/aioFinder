from sqlalchemy import select, func, desc

from message_schema import Updater
from plugins.systems import Systems
from plugins.config import cfg
from plugins.helper import send_message
from plugins.helper import remove_html_in_dict
from plugins.pg.tables import index_map, cache_index, vacancy_content


# TODO сделать прокси класс с коннекторами в базе и кэшу
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
    await send_message(cfg.app.hosts.tlg.host,
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
    if m.message.text != 'Нет':
        if await systems.local_cache.check(m.message.chat.id):
            # TODO подумать, нужно ли так рано
            await systems.local_cache.next_step(m.message.chat.id)
        else:
            # возвращат id вакансии
            # запрос к базе данный
            times = select([index_map.c.original_index]).\
                where(index_map.c.extended_index == m.message.text).\
                alias("times")

            j = times.join(cache_index, times.c.original_index == cache_index.c.original_index)

            search_result = select([cache_index.c.vacancy_id, func.count(cache_index.c.vacancy_id).label('counter')]). \
                select_from(j). \
                group_by(cache_index.c.vacancy_id).\
                order_by(desc('counter')).\
                alias("search_result")

            j = search_result.join(vacancy_content, search_result.c.vacancy_id == vacancy_content.c.id)

            query = select([search_result, vacancy_content]).select_from(j).order_by(
                desc(search_result.c.counter)).limit(5)

            ready_content = []
            columns = ["id", "title", "footer", "header",
                       "requirements", "duties", "conditions",
                       "date", "locality", "region", "company"]
            for row in await systems.pg.fetch(query):
                reconstruction: dict = {v: str(row[v]) for v in columns}
                ready_content.append(reconstruction)
            step = 0
            await systems.local_cache.caching(m.message.chat.id,
                                              step=step,
                                              arr=ready_content)
        most_sim_vacancy_content = await systems.local_cache.give_cache(m.message.chat.id)
        if most_sim_vacancy_content:
            title: str = "💥 Название позиции: " + most_sim_vacancy_content['title'] + '\n'
            text: str = title + "💥 Описание: " + most_sim_vacancy_content['header'] + '\n' + \
                        cfg.app.hosts.sbervacanсy.host.format(str(most_sim_vacancy_content['id']))
            text: str = text + '\n' "Показать еще❓"
            await send_message(cfg.app.hosts.tlg.host, m.message.chat.id,
                               remove_html_in_dict(text)[:4095],
                               buttons=['Да', 'Нет'],
                               one_time_keyboard=False)
            return 1
        else:
            text = '🤓 К сожалению, вакансий больше нет❗️'
            await send_message(cfg.app.hosts.tlg.host,
                               m.message.chat.id,
                               text,
                               remove_keyboard=True)
            return 0

    else:
        text = '💥 Пока, возвращайся еще❗️'
        await send_message(cfg.app.hosts.tlg.host,
                           m.message.chat.id,
                           text,
                           remove_keyboard=True)
        return 0


async def goodbye_message(m: Updater):
    text = '💥 Пока, возвращайся еще❗️'
    await send_message(cfg.app.hosts.tlg.host,
                       m.message.chat.id,
                       text,
                       remove_keyboard=True)
    return 0
