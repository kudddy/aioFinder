import asynctest
from plugins.cache import AioMemCache
from plugins.config import cfg


class AioMemTest(asynctest.TestCase):
    async def test_get_and_set_from_cache(self):
        mc = AioMemCache()

        value: dict = {"1": 2}

        await mc.set(123, value)

        res = await mc.get(123)

        self.assertEqual(value, res)
