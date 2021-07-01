import asynctest
import logging

from time import sleep

from plugins.config import cfg
from plugins.statemachine import Stages
from plugins.callback import hello_message, analyze_text_and_give_vacancy, goodbye_message
from plugins.cache import AioMemCache

from message_schema import Updater

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


# mc = AioMemCache()
#
# state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}
#
# stage = Stages(state, mc)

class TestInternalSystem(asynctest.TestCase):
    async def test_positive_node(self):
        mc = AioMemCache()

        mc.cache.flush_all()

        state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

        stage = Stages(state, mc)

        log.debug("checking a positive thread when the user follows all the recommendations")
        log.debug("phrase check - hello")

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
                "text": "hello"
            }
        }

        message = Updater(**data)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        log.debug("phrase check - python")
        log.debug("we remain in the same state, but go through all the recommendations")

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

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        log.debug("phrase check - yes")
        log.debug("we answer yes to the question continue to show the recommendations that are stored in the cache")

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
                "text": "да"
            }
        }

        message = Updater(**data)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        log.debug("phrase check - no")
        log.debug("we answer the question no and reset the user state")

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
                "text": "Нет"
            }
        }

        message = Updater(**data)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 0)

        mc.cache.close()

    async def test_node_with_timeout(self):
        mc = AioMemCache()

        mc.cache.flush_all()

        state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

        stage = Stages(state, mc)

        log.debug("checking a positive thread when the user follows all the recommendations")
        log.debug("phrase check - hello")

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
                "text": "hello"
            }
        }

        message = Updater(**data)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        log.debug("phrase check - python")
        log.debug("we remain in the same state, but go through all the recommendations")

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

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        log.debug("phrase check - yes")
        log.debug("we remain in the same state, but go through all the recommendations, but timeout")

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

        sleep(cfg.app.constants.timeout_for_chat_test + 2)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        mc.cache.close()
