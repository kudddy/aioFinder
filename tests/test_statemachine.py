import asynctest
import logging
from asyncpgsa import PG
from aiomcache import Client
from time import sleep

from plugins.config import cfg
from plugins.tools.tokenizer import QueryBuilder
from plugins.statemachine import Stages
from plugins.systems import Systems, LocalCacheForCallbackFunc
from plugins.callback import hello_message, analyze_text_and_give_vacancy, goodbye_message
from plugins.mc.init import AioMemCache

from message_schema import Updater

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


class TestInternalSystem(asynctest.TestCase):
    async def test_node_with_timeout(self):
        # Инициализируем соедением с mc
        memcached = Client(
            cfg.app.hosts.mc.host,
            cfg.app.hosts.mc.port,
            pool_size=2)

        global_cache = AioMemCache(memcached)

        # Инициализируем соединение с базой данных
        pg = PG()

        pg_pool_min_size = 10
        pg_pool_max_size = 10

        await pg.init(
            str(cfg.app.hosts.pg.url),
            min_size=pg_pool_min_size,
            max_size=pg_pool_max_size
        )

        # Инициализируем локальный кэш для кэширования запросов к базе данных

        local_cache = LocalCacheForCallbackFunc(global_cache)

        global_cache.cache.flush_all()

        state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

        tokenizer = QueryBuilder(out_clean='str', out_token='list')

        system = Systems(mc=global_cache,
                         pg=pg,
                         local_cache=local_cache,
                         tokenizer=tokenizer)

        stage = Stages(state, system)

        memcached.flush_all()

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

        sleep(cfg.app.constants.timeout_for_chat + 2)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        memcached.flush_all()

        sleep(cfg.app.constants.timeout_for_chat + 2)

    async def test_positive_node(self):
        # Инициализируем соедением с mc
        memcached = Client(
            cfg.app.hosts.mc.host,
            cfg.app.hosts.mc.port,
            pool_size=2)

        global_cache = AioMemCache(memcached)

        # Инициализируем соединение с базой данных
        pg = PG()

        pg_pool_min_size = 10
        pg_pool_max_size = 10

        await pg.init(
            str(cfg.app.hosts.pg.url),
            min_size=pg_pool_min_size,
            max_size=pg_pool_max_size
        )

        # Инициализируем локальный кэш для кэширования запросов к базе данных

        local_cache = LocalCacheForCallbackFunc(global_cache)

        state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

        tokenizer = QueryBuilder(out_clean='str', out_token='list')

        system = Systems(mc=global_cache,
                         pg=pg,
                         local_cache=local_cache,
                         tokenizer=tokenizer)

        stage = Stages(state, system)

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
                "text": "Привет"
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
                "text": "Да"
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

        global_cache.cache.close()
