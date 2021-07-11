from aiohttp.web_app import Application

from message_schema import Updater

from plugins.config import cfg
from plugins.systems import Systems
from plugins.systems import LocalCacheForCallbackFunc
from plugins.tools.tokenizer import QueryBuilder
from plugins.mc.init import AioMemCache
from plugins.callback import hello_message, analyze_text_and_give_vacancy, goodbye_message


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
        chat_id = m.get_chat_id()
        key = await self.systems.global_cache.get(chat_id)
        if key:
            step = int(key['step'])
        else:
            step = 0

        step = await self.stages[step].__call__(m, self.systems)
        key = await self.systems.global_cache.get(chat_id)

        if key:
            key['step'] = step
        else:
            key = {'step': step}

        await self.systems.global_cache.set(chat_id, key, cfg.app.constants.timeout_for_chat)
        # возвращаем результат для тестирования навыка
        return step


async def init_stages(app: Application):
    # коллбэк функции
    state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}
    # коннектор к базе данных
    global_cache = AioMemCache(app['mc'])
    # инициализация локального кэша для реализации возможности кэшировать запросы к базе данных
    # TODO переименовать, т.к. по факту служит кэшем только для одного запроса
    local_cache = LocalCacheForCallbackFunc(global_cache)
    # инициализируем токенизер
    tokenizer = QueryBuilder(out_clean='str', out_token='list')
    # Инициализация прокси объекта с объектами, которые нужны для сценария
    # TODO нейминг выглядит хуева
    systems = Systems(mc=global_cache,
                      pg=app['pg'],
                      local_cache=local_cache,
                      tokenizer=tokenizer)

    app['stage'] = Stages(state, systems)
