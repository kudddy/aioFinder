# from plugins.cache import AioMemCache
# from plugins.config import cfg
# import inspect
# #
# # # mc.set("123", {"123": "123"})
# # #
# # # a = mc.get("123")
# #
# # # print(a)
# #
# import asyncio
# import aiomcache
#
# loop = asyncio.get_event_loop()
#
# mc = AioMemCache(host=cfg.app.hosts.mc.host,
#                  port=cfg.app.hosts.mc.port,
#                  loop=loop)
#
#
# async def hello_aiomcache():
#     await mc.set(123, {"1": 2})
#     value = await mc.get(123)
#     print(value)
#     # values = await mc.multi_get(b"some_key", b"other_key")
#     # print(values)
#     # await mc.delete(b"another_key")
#
#
# loop.run_until_complete(hello_aiomcache())

# mc = AioMemCache(host=cfg.app.hosts.mc.host,
#                  port=cfg.app.hosts.mc.port,
#                  loop=loop)
# if isinstance(mc, AioMemCache):
#     print("dsfdsfsf")

# import time
# from functools import wraps
#
# from plugins.helper import Coder
#
# import inspect
# from inspect import isclass
#
# mylist = [1, 4, -5, 10, -7, 2, 3, -1]
#
# clip_neg = [n if n > 0 else 0 for n in mylist]
#
#
# def timethis(func):
#     @wraps(func)
#     def wrapper(*args):
#         start = time.time()
#         for x in args:
#             print("что на входе:{}".format(x))
#         result = func(*tuple([x * 2 if isclass(x) else x for x in args]))
#         end = time.time()
#         print(func.__name__, end - start)
#         return result
#
#     return wrapper
#
#
# class Test:
#     def __init__(self, b: int):
#         self.b = b
#
#     @timethis
#     def countdown(self, n):
#         print(self.b)
#         while n > 0:
#             n -= 1
#
#
# test = Test(b=100)
#
# test.countdown(100000)
#
# print(inspect.isclass(Test))

a = b'300'

print(int(a))
