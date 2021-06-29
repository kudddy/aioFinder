from typing import List

from message_schema import Updater

from plugins.config import cfg
from plugins.cache import mc


class Stages:
    def __init__(self, stages):
        self.stages = stages

    @property
    def k_iter(self):
        return len(self.stages) - 1

    async def next(self, m: Updater) -> None:
        """
        Ф-ция занимается маршрутизацией и вызовом коллбэк функций
        :param m: сообщение от Telegram
        :return: None
        """
        if m.message:
            chat_id = m.message.chat.id
        else:
            chat_id = m.callback_query.message.chat.id
        key = await mc.get(chat_id)
        if key:
            step = int(key['step'])
        else:
            step = 0

        step = await self.stages[step].__call__(m)

        key = await mc.get(chat_id)

        if key:
            key['step'] = step
        else:
            key = {'step': step}

        await mc.set(chat_id, key, cfg.app.constants.timeout_for_chat)


class LocalCacheForCallbackFunc:

    @staticmethod
    async def caching(chat_id: int, step: int, arr: List[int]) -> None:

        val = await mc.get(chat_id)

        val['cache_vacancy_result'] = arr
        val['cache_iter'] = step

        await mc.set(chat_id, val)

    @staticmethod
    async def give_cache(chat_id: int) -> int or False:
        val = await mc.get(chat_id)
        if val:
            try:
                return val['cache_vacancy_result'][val['cache_iter']]
            except IndexError as e:
                return False
        else:
            return False

    @staticmethod
    async def check(chat_id: int) -> bool:
        val = await mc.get(chat_id)
        if 'cache_iter' in val:
            return True
        else:
            return False

    @staticmethod
    async def clean(chat_id: int) -> None:
        val = await mc.get(chat_id)
        if val:
            await mc.delete(chat_id)

    @staticmethod
    async def next_step(chat_id: int) -> None:
        val = await mc.get(chat_id)
        val['cache_iter'] += 1
        await mc.set(chat_id, val)
