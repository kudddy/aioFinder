import aiomcache
import logging
from functools import wraps

from plugins.config import cfg
from plugins.helper import Coder

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


def encode_input_value(func):
    # TODO есть впечатление что операция блокирующая
    @wraps(func)
    async def wrapper(*args):
        result = await func(*tuple(Coder.encode(x) if not isinstance(x, AioMemCache) else x for x in args))
        if result:
            return Coder.decode(result)

    return wrapper


class AioMemCache:
    def __init__(self, host: str, port: int, loop=None):
        try:
            self.cache = aiomcache.Client(
                host,
                port,
                loop=loop,
                pool_size=2)
            log.debug("Success connect to %r - %r",
                      host,
                      port)
        except Exception as e:
            log.debug("Error to connect memcached with address %r - %r, error - %r",
                      host,
                      port,
                      e)

    @encode_input_value
    async def get(self, key: object):
        value = await self.cache.get(key)
        return value

    @encode_input_value
    async def set(self, key: object, value: object, timeout: int = 0):
        await self.cache.set(key, value, exptime=int(timeout))

    @encode_input_value
    async def delete(self, key: object):
        await self.cache.delete(key)


mc = AioMemCache(host=cfg.app.hosts.mc.host,
                 port=cfg.app.hosts.mc.port)
