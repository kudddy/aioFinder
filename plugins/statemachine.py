from aiohttp.web_app import Application

from message_schema import Updater

from plugins.config import cfg
from plugins.systems import Systems
from plugins.systems import LocalCacheForCallbackFunc
from plugins.tools.tokenizer import QueryBuilder
from plugins.mc.init import AioMemCache
from plugins.classifier import Model
from plugins.callback import hello_message, get_vacancy, \
    add_vacancy_to_favorites, history_viewed_vacancy, \
    viewed_history_already_cleaned, add_vacancy_to_history, \
    show_favor_vacancy, return_to_init_state, \
    uncover_vacancy_info, get_extend_vacancy, nothing_found


class Stages:
    def __init__(self,
                 stages: dict,
                 systems: Systems):
        self.stages = stages
        self.systems = systems

    @property
    def k_iter(self):
        return len(self.stages) - 1

    async def next(self,
                   m: Updater) -> int:
        """
        Ф-ция занимается маршрутизацией и вызовом коллбэк функций
        :param m: сообщение от Telegram
        :return: None
        """
        text = m.get_text()
        chat_id = m.get_chat_id()
        # запрашиваем глобальный кэш
        key = await self.systems.global_cache.get(chat_id)
        # если есть то смотрим на шаг
        if key:
            # если сессия активирована,то запускаем классификатор
            step = self.systems.model.predict(text=text)
        # если нет, то в начальном стейте
        else:
            step = 0

        # вызываем функцию соответствующу стейту
        await self.stages[step].__call__(m, self.systems)

        # достаем сессионные данные
        key = await self.systems.global_cache.get(chat_id)

        # если пользователь уже в стейте, то перезаписываем стейт
        if key:
            key['step'] = step
        else:
            # если нет, то создаем новый
            key = {'step': step}

        # записываем обновленные данные по сессии
        await self.systems.global_cache.set(chat_id, key, cfg.app.constants.timeout_for_chat)
        # возвращаем результат для тестирования навыка
        return step


async def init_stages(app: Application):
    # требуется внедрить классификатор входящих интентов, которые возвращают стейт сценари
    train_data: dict = {
        "Следующая": 1,
        "В избранное": 2,
        "Очистить": 3,
        "Очистил": 4,
        "Добавил": 5,
        "Избранное": 6,
        "В начало": 0,
        "Раскрыть": 8,
        "Расширенный": 9
    }
    # коллбэк функции
    model = Model()

    model.fit(train_data)

    state = {
        0: hello_message,
        1: get_vacancy,
        2: add_vacancy_to_favorites,
        3: history_viewed_vacancy,
        4: viewed_history_already_cleaned,
        5: add_vacancy_to_history,
        6: show_favor_vacancy,
        7: return_to_init_state,
        8: uncover_vacancy_info,
        9: get_extend_vacancy,
        10: nothing_found
    }
    # коннектор к базе данных
    mc = AioMemCache(app['mc'])
    # инициализация локального кэша для реализации возможности кэшировать запросы к базе данных
    # TODO переименовать, т.к. по факту служит кэшем только для одного запроса
    local_cache = LocalCacheForCallbackFunc(mc)
    # инициализируем токенизер
    tokenizer = QueryBuilder(out_clean='str', out_token='list')
    # Инициализация прокси объекта с объектами, которые нужны для сценария
    # TODO нейминг выглядит хуева
    systems = Systems(mc=mc,
                      pg=app['pg'],
                      local_cache=local_cache,
                      tokenizer=tokenizer,
                      model=model)

    app['stage'] = Stages(state, systems)
