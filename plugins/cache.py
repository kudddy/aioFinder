import aiomcache
import logging
from functools import wraps
from typing import List

from plugins.config import cfg
from plugins.helper import Coder

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.setLevel(logging.INFO)


def encode_input_value(func):
    # TODO есть впечатление что операция блокирующая
    @wraps(func)
    async def wrapper(*args):
        result = await func(*tuple(Coder.encode(x) if not isinstance(x, AioMemCache) else x for x in args))
        if result:
            return Coder.decode(result)

    return wrapper


class AioMemCache:
    def __init__(self):
        try:
            self.cache = aiomcache.Client(
                cfg.app.hosts.mc.host,
                cfg.app.hosts.mc.port,
                pool_size=2)
            log.debug("Success connect to %r - %r",
                      cfg.app.hosts.mc.host,
                      cfg.app.hosts.mc.port)
        except Exception as e:
            log.debug("Error to connect memcached with address %r - %r, error - %r",
                      cfg.app.hosts.mc.host,
                      cfg.app.hosts.mc.port,
                      e)

    # @encode_input_value
    async def get(self, key: object):
        value = await self.cache.get(Coder.encode(key))
        if value:
            value = Coder.decode(value)
        return value

    # @encode_input_value
    async def set(self, key: object, value: object, timeout: int = 0):
        await self.cache.set(Coder.encode(key), Coder.encode(value), exptime=timeout)

    # @encode_input_value
    async def delete(self, key: object):
        await self.cache.delete(Coder.encode(key))


class LocalCacheForCallbackFunc:
    def __init__(self, cache: AioMemCache):
        self.mc = cache

    async def caching(self, chat_id: int, step: int, arr: List[int]) -> None:

        val = await self.mc.get(chat_id)

        val['cache_vacancy_result'] = arr
        val['cache_iter'] = step

        await self.mc.set(chat_id, val)

    async def give_cache(self, chat_id: int) -> int or False:
        val = await self.mc.get(chat_id)
        if val:
            try:
                return val['cache_vacancy_result'][val['cache_iter']]
            except IndexError as e:
                return False
        else:
            return False

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
        val['cache_iter'] += 1
        await self.mc.set(chat_id, val)
# mc = AioMemCache(host=cfg.app.hosts.mc.host,
#                  port=cfg.app.hosts.mc.port)
