from typing import List
from asyncpgsa import PG
from plugins.mc.init import AioMemCache
from plugins.tools.tokenizer import QueryBuilder


class LocalCacheForCallbackFunc:
    """
    Плагин для реализации механизма кэширования запросов к базе данных
    """

    def __init__(self, cache: AioMemCache):
        self.mc = cache

    async def caching(self, chat_id: int, step: int, is_likes_display: bool, arr: List) -> None:

        val = await self.mc.get(chat_id)
        if val:
            val['cache_vacancy_result'] = arr
            val['cache_iter'] = step,
            val['is_likes_display'] = is_likes_display
        else:
            val = {
                'cache_vacancy_result': arr,
                'cache_iter': step,
                'is_likes_display': is_likes_display
            }

        await self.mc.set(chat_id, val)

    async def give_cache(self, chat_id: int) -> int or False:
        """
        Возвращает содер
        :param chat_id:
        :return:
        """
        val = await self.mc.get(chat_id)
        if val:
            try:
                return val['cache_vacancy_result'][val['cache_iter'][0]], val['is_likes_display']
            except IndexError as e:
                return False, False
        else:
            return False, False, False

    async def check(self, chat_id: int) -> bool:
        val = await self.mc.get(chat_id)
        if 'cache_iter' in val:
            return True
        else:
            return False

    async def clean(self, chat_id: int) -> None:
        val = await self.mc.get(chat_id)
        if val:
            await self.mc.delete(chat_id)

    async def next_step(self, chat_id: int) -> None:
        val = await self.mc.get(chat_id)
        val['cache_iter'][0] += 1
        await self.mc.set(chat_id, val)


class Systems:
    """
    Плагин прокси объект, которые дает доступ к операциям с базами данных
    """

    def __init__(self, mc: AioMemCache,
                 pg: PG,
                 local_cache: LocalCacheForCallbackFunc,
                 tokenizer: QueryBuilder):
        self.global_cache = mc
        self.pg = pg
        self.local_cache = local_cache
        self.tokenizer = tokenizer
