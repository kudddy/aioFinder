import html2text
from datetime import datetime
from message_schema import Updater
from plugins.systems import Systems
from plugins.config import cfg
from plugins.helper import send_message, edit_message
from plugins.pg.query import generate_search_query
from plugins.pg.tables import user_enter


async def hello_message(m: Updater,
                        systems: Systems):
    """
    Приветственное сообщение с просьбой указать навык
    :param systems: Объект с вспомогательными классами(для доступа к базам и локальному кэшу)
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """

    chat_id = m.get_chat_id()
    user_id = m.get_user_id()

    await systems.local_cache.clean(chat_id)

    text = "💥 Приветствую, я найду для тебя работу. Введите свой ключевой навык❗"
    inline_keyboard = [
        [
            {
                "text": "JavaScript",
                "callback_data": "JavaScript"
            },
            {
                "text": "Python",
                "callback_data": "Python"

            },
        ],
        [
            {
                "text": "Java, Scala",
                "callback_data": "Java, Scala"
            },
            {
                "text": "C/C++, Assembler",
                "callback_data": "C/C++, Assembler"
            }
        ],
        [
            {
                "text": "PHP",
                "callback_data": "PHP"
            },
            {
                "text": ".NET",
                "callback_data": ".NET"
            },
            {
                "text": "QA",
                "callback_data": "QA"
            }
        ],
        [
            {
                "text": "DevOps",
                "callback_data": "DevOps"
            },
            {
                "text": "IOS",
                "callback_data": "IOS"
            },
            {
                "text": "Golang",
                "callback_data": "Golang"
            }
        ],
        [
            {
                "text": "Data Science",
                "callback_data": "DS, Data Science"
            },
            {
                "text": "Security",
                "callback_data": "Security, безопасность"
            },
        ],
        [
            {
                "text": "Analyst",
                "callback_data": "Analyst"
            },
            {
                "text": "Manager",
                "callback_data": "Manager"
            }
        ]

    ]
    await send_message(cfg.app.hosts.tlg.send_message,
                       chat_id,
                       text,
                       inline_keyboard=inline_keyboard)

    query = user_enter.insert().values(
        user_id=user_id,
        chat_id=chat_id,
        date=datetime.now()
    )

    await systems.pg.fetch(query)

    return 1


async def analyze_text_and_give_vacancy(m: Updater,
                                        systems: Systems):
    """
    :param systems: Объект с вспомогательными функциями(для доступа к базам, локальному кэшу и др)
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    chat_id = m.get_chat_id()
    message_id = m.get_message_id()
    user_id = m.get_user_id()
    text = m.get_text()
    # Подразумевается что пользователь уже вбил критерий поиска
    # TODO операцию можно выполнить один раз
    if await systems.local_cache.check(chat_id):
        # продолжаем итерировать по списку вакансий
        if text == "Следующая":
            # TODO переименовать чтобы было более наглядно что мы вытаскваем инфо по вакансии
            await systems.local_cache.next_step(chat_id)

            most_sim_vacancy_content = await systems.local_cache.give_cache(chat_id)
            if most_sim_vacancy_content:

                # TODO обратить внимание на форматирование

                # todo сделать датакласс

                url: str = cfg.app.hosts.sbervacanсy.host.format(most_sim_vacancy_content["id"])

                inline_keyboard = [
                    [
                        {
                            "text": "Следующая",
                            "callback_data": "Следующая"
                        },
                        {
                            "text": "Вернуться к выбору категории",
                            "callback_data": "В начало"

                        },
                    ],
                    [
                        {
                            "text": "Описание и отклик",
                            "url": url,
                            "callback_data": ""
                        }
                    ]
                ]
                # todo преобразовывать из html в text на уровне загрузки данных в базу

                title: str = "💥 Название позиции: " + most_sim_vacancy_content['title'] + '\n'
                txt: str = title + "💥 Описание: " + html2text.html2text(most_sim_vacancy_content['header'])[
                                                      :4000] + '\n'
                txt: str = txt + '\n' "Показать еще❓"

                await edit_message(url=cfg.app.hosts.tlg.edit_message,
                                   text=txt,
                                   message_id=message_id,
                                   chat_id=chat_id,
                                   inline_keyboard=inline_keyboard)

                # отправляем в базу инфо по поводу оценки пользователя касательно вакансии

                return 1
            else:
                text = '🤓 К сожалению, вакансий больше нет❗️'
                await send_message(cfg.app.hosts.tlg.send_message,
                                   chat_id,
                                   text,
                                   remove_keyboard=True)
                return 0
        # переводим клиента на экран с выбором категории поиска
        elif text == "Вначало":
            await hello_message(m, systems)
            return 1
        # заканчиваем диалог
        else:
            text = '💥 Пока, возвращайся еще❗️'
            await send_message(cfg.app.hosts.tlg.send_message,
                               chat_id,
                               text,
                               remove_keyboard=True)
            return 0

    else:

        list_of_tokens: list = systems.tokenizer.clean_query(text)
        query = generate_search_query(list_of_tokens)

        ready_content = []
        # columns = ["id", "title", "footer", "header",
        #            "requirements", "duties", "conditions",
        #            "date", "locality", "region", "company"]
        # TODO грязный баг фикс, который умешает размер объекта в кэше
        columns = ["id", "title", "header"]
        for row in await systems.pg.fetch(query):
            reconstruction: dict = {v: str(row[v]) for v in columns}
            ready_content.append(reconstruction)
        step = 0
        await systems.local_cache.caching(chat_id,
                                          step=step,
                                          arr=ready_content)
        # первый раз отсылаем сообщение
        if len(ready_content) > 0:

            url: str = cfg.app.hosts.sbervacanсy.host.format(ready_content[step]["id"])

            inline_keyboard = [
                [
                    {
                        "text": "Лайк",
                        "callback_data": "Лайк"
                    },
                    {
                        "text": "Дизлайк",
                        "callback_data": "Дизлайк"

                    }
                ],
                [
                    {
                        "text": "Описание и отклик",
                        "url": url,
                        "callback_data": ""
                    }
                ],
                [
                    {
                        "text": "Вернуться к выбору категории",
                        "callback_data": "Вначало"
                    }
                ]

            ]
            # генерируем текст сообщения
            title: str = "💥 Название позиции: " + ready_content[step]['title'] + '\n'
            text: str = title + "💥 Описание: " + html2text.html2text(ready_content[step]['header'])[:4000] + '\n'
            text: str = text + '\n' "Показать еще❓"

            await send_message(cfg.app.hosts.tlg.send_message,
                               chat_id,
                               text,
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
                       m.get_chat_id(),
                       text,
                       remove_keyboard=True)
    return 0
