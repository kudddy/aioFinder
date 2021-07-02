from message_schema import Updater

from plugins.config import cfg
from plugins.cache import AioMemCache, LocalCacheForCallbackFunc


class Stages:
    def __init__(self,
                 stages: dict,
                 cache: AioMemCache):
        self.stages = stages
        self.mc = cache
        self.memo = LocalCacheForCallbackFunc(cache)

    @property
    def k_iter(self):
        return len(self.stages) - 1

    async def next(self, m: Updater) -> int:
        """
        Ф-ция занимается маршрутизацией и вызовом коллбэк функций
        :param m: сообщение от Telegram
        :return: None
        """
        if m.message:
            chat_id = m.message.chat.id
        else:
            chat_id = m.callback_query.message.chat.id
        key = await self.mc.get(chat_id)
        if key:
            step = int(key['step'])
        else:
            step = 0

        step = await self.stages[step].__call__(m, self.memo)

        key = await self.mc.get(chat_id)

        if key:
            key['step'] = step
        else:
            key = {'step': step}

        await self.mc.set(chat_id, key, cfg.app.constants.timeout_for_chat)
        # возвращаем результат для тестирования навыка
        return step



