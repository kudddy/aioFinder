import unittest
import asyncio
from time import sleep

import aiounittest

from plugins.cache import AioMemCache
from plugins.config import cfg
from plugins.statemachine import Stages
from plugins.callback import hello_message, analyze_text_and_give_vacancy, goodbye_message

from message_schema import Updater

# loop = asyncio.get_event_loop()


state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

stage = Stages(state)


class AioMemTest(aiounittest.AsyncTestCase):

    async def test_get_and_set_from_cache(self):
        mc = AioMemCache(host=cfg.app.hosts.mc.host,
                         port=cfg.app.hosts.mc.port)

        value: dict = {"1": 2}
        await mc.set(123, value)

        res: dict = await mc.get(123)

        self.assertEqual(res, value)


class TestInternalSystem(unittest.TestCase):
    maxDiff = None

    async def test_message_valid_form_user_one(self):
        data = {
            "update_id": 243475549,
            "message": {
                "message_id": 9450,
                "from": {
                    "id": 81432612,
                    "is_bot": False,
                    "first_name": "Kirill",
                    "username": "kkkkk_kkk_kkkkk",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 81432612,
                    "first_name": "Kirill",
                    "username": "kkkkk_kkk_kkkkk",
                    "type": "private"
                },
                "date": 1589404439,
                "text": "python"
            }
        }

        message = Updater(**data)

        await stage.next(message)

        await stage.next(message)

        await stage.next(message)

        sleep(cfg.app.constants.timeout_for_chat_test + 2)

        await stage.next(message)

    async def test_message_valid_form_user_two(self):
        data = {
            "update_id": 632560263,
            "message": {
                "message_id": 505,
                "from": {
                    "id": 710828013,
                    "is_bot": False,
                    "first_name": "Серега",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 710828013,
                    "first_name": "Серега",
                    "type": "private"
                },
                "date": 1600629554,
                "text": "java"
            }
        }

        message = Updater(**data)

        await stage.next(message)

        await stage.next(message)

        await stage.next(message)
        data = {
            "update_id": 632560263,
            "message": {
                "message_id": 505,
                "from": {
                    "id": 710828013,
                    "is_bot": False,
                    "first_name": "Серега",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 710828013,
                    "first_name": "Серега",
                    "type": "private"
                },
                "date": 1600629554,
                "text": "Нет"
            }
        }

        message = Updater(**data)

        await stage.next(message)

        sleep(cfg.app.constants.timeout_for_chat_test + 2)

        await stage.next(message)

# if __name__ == "__main__":
#     loop.run_until_complete(unittest.main())
