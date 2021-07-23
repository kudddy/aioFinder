from datetime import datetime
from message_schema import Updater
from plugins.systems import Systems
from plugins.config import cfg
from plugins.helper import send_message, edit_message, generate_message_body
from plugins.pg.query import generate_search_query, sorting_by_viewed_vacancies, main_search_query, give_me_likes_vacancy
from plugins.pg.tables import user_enter, likes_info, viewed_vacancy
from plugins.keybords import inline_keyboard_for_hello, \
    generate_pagination_keyboard, generate_check_box_keyboard, \
    generate_emo_keyboard, generate_check_box_for_clean, generate_keyboard_for_likes


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
    username = m.get_username()

    await systems.local_cache.clean(chat_id)

    text = "💥 Приветствую, я найду для тебя работу. Введите свой ключевой навык❗"

    await send_message(cfg.app.hosts.tlg.send_message,
                       chat_id,
                       text,
                       inline_keyboard=inline_keyboard_for_hello)

    query = user_enter.insert().values(
        user_id=user_id,
        chat_id=chat_id,
        username=username,
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
    text = m.get_text()
    # Подразумевается что пользователь уже вбил критерий поиска
    # TODO операцию можно выполнить один раз
    if await systems.local_cache.check(chat_id):
        # продолжаем итерировать по списку вакансий
        if text == "Следующая":

            # TODO переименовать чтобы было более наглядно что мы вытаскваем инфо по вакансии
            await systems.local_cache.next_step(chat_id)

            most_sim_vacancy_content, is_likes_display = await systems.local_cache.give_cache(chat_id)
            if most_sim_vacancy_content:

                # TODO обратить внимание на форматирование

                # todo сделать датакласс

                url: str = cfg.app.hosts.sbervacanсy.host.format(most_sim_vacancy_content["id"])

                # todo преобразовывать из html в text на уровне загрузки данных в базу

                message_body: str = generate_message_body(most_sim_vacancy_content)

                if is_likes_display:
                    await edit_message(url=cfg.app.hosts.tlg.edit_message,
                                       text=message_body,
                                       message_id=message_id,
                                       chat_id=chat_id,
                                       inline_keyboard=generate_keyboard_for_likes(url))

                else:
                    await edit_message(url=cfg.app.hosts.tlg.edit_message,
                                       text=message_body,
                                       message_id=message_id,
                                       chat_id=chat_id,
                                       inline_keyboard=generate_pagination_keyboard(url))

                # Пишем уже просмотренные вакансии
                query = viewed_vacancy.insert().values(
                    user_id=m.get_user_id(),
                    chat_id=chat_id,
                    date=datetime.now(),
                    vacancy_id=int(most_sim_vacancy_content["id"])
                )

                await systems.pg.fetch(query)

                return 1
            else:
                text = '🤓 К сожалению, вакансий больше нет❗️'
                await send_message(cfg.app.hosts.tlg.send_message,
                                   chat_id,
                                   text,
                                   remove_keyboard=True)
                return 0
        elif text == "В избранное":

            most_sim_vacancy_content, _ = await systems.local_cache.give_cache(chat_id)

            url: str = cfg.app.hosts.sbervacanсy.host.format(most_sim_vacancy_content["id"])

            # todo преобразовывать из html в text на уровне загрузки данных в базу

            message_body: str = generate_message_body(most_sim_vacancy_content)

            await edit_message(url=cfg.app.hosts.tlg.edit_message,
                               text=message_body,
                               message_id=message_id,
                               chat_id=chat_id,
                               inline_keyboard=generate_check_box_keyboard(url))

            query = likes_info.insert().values(
                user_id=m.get_user_id(),
                chat_id=chat_id,
                date=datetime.now(),
                vacancy_id=int(most_sim_vacancy_content["id"])
            )

            await systems.pg.fetch(query)

            return 1
        elif text == "Очистить":
            query = viewed_vacancy.delete().where(viewed_vacancy.c.chat_id == chat_id)

            await systems.pg.fetch(query)

            most_sim_vacancy_content, _ = await systems.local_cache.give_cache(chat_id)

            url: str = cfg.app.hosts.sbervacanсy.host.format(most_sim_vacancy_content["id"])

            message_body: str = generate_message_body(most_sim_vacancy_content)

            await edit_message(url=cfg.app.hosts.tlg.edit_message,
                               text=message_body,
                               message_id=message_id,
                               chat_id=chat_id,
                               inline_keyboard=generate_check_box_for_clean(url))

            return 1

        elif text == "Очистил":
            # очищаем историю просмотров

            most_sim_vacancy_content, _ = await systems.local_cache.give_cache(chat_id)

            url: str = cfg.app.hosts.sbervacanсy.host.format(most_sim_vacancy_content["id"])

            message_body: str = generate_message_body(most_sim_vacancy_content)

            await edit_message(url=cfg.app.hosts.tlg.edit_message,
                               text=message_body,
                               message_id=message_id,
                               chat_id=chat_id,
                               inline_keyboard=generate_check_box_for_clean(url, double_click=True))
            return 1

        elif text == "Добавил":
            most_sim_vacancy_content, _ = await systems.local_cache.give_cache(chat_id)

            url: str = cfg.app.hosts.sbervacanсy.host.format(most_sim_vacancy_content["id"])

            message_body: str = generate_message_body(most_sim_vacancy_content)

            await edit_message(url=cfg.app.hosts.tlg.edit_message,
                               text=message_body,
                               message_id=message_id,
                               chat_id=chat_id,
                               inline_keyboard=generate_emo_keyboard(url))

            return 1

        elif text == "Избранное":
            query = give_me_likes_vacancy(chat_id)
            ready_content = []
            columns = ["id", "title", "header"]
            for row in await systems.pg.fetch(query):
                reconstruction: dict = {v: str(row[v]) for v in columns}
                ready_content.append(reconstruction)
            step = 0
            await systems.local_cache.caching(chat_id,
                                              step=step,
                                              is_likes_display=True,
                                              arr=ready_content)

            message_body = generate_message_body(ready_content[step])

            url: str = cfg.app.hosts.sbervacanсy.host.format(ready_content[step]["id"])

            await send_message(cfg.app.hosts.tlg.send_message,
                               chat_id,
                               message_body,
                               inline_keyboard=generate_keyboard_for_likes(url))

            return 1

        # переводим клиента на экран с выбором категории поиска
        elif text == "В начало":
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
        query = main_search_query(list_of_tokens)

        query = sorting_by_viewed_vacancies(query)

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
                                          is_likes_display=False,
                                          arr=ready_content)
        # первый раз отсылаем сообщение
        if len(ready_content) > 0:

            url: str = cfg.app.hosts.sbervacanсy.host.format(ready_content[step]["id"])

            message_body = generate_message_body(ready_content[step])

            await send_message(cfg.app.hosts.tlg.send_message,
                               chat_id,
                               message_body,
                               inline_keyboard=generate_pagination_keyboard(url))

            # Пишем уже просмотренные вакансии
            query = viewed_vacancy.insert().values(
                user_id=m.get_user_id(),
                chat_id=chat_id,
                date=datetime.now(),
                vacancy_id=int(ready_content[step]["id"])
            )

            await systems.pg.fetch(query)
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
