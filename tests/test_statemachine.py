import asynctest
import logging
from asyncpgsa import PG
from aiomcache import Client
from time import sleep

from plugins.config import cfg
from plugins.tools.tokenizer import QueryBuilder
from plugins.statemachine import Stages
from plugins.systems import Systems, LocalCacheForCallbackFunc
from plugins.mc.init import AioMemCache
from plugins.classifier import Model
from plugins.callback import hello_message, get_vacancy, \
    add_vacancy_to_favorites, history_viewed_vacancy, \
    viewed_history_already_cleaned, add_vacancy_to_history, \
    show_favor_vacancy, return_to_init_state, \
    uncover_vacancy_info, get_extend_vacancy, nothing_found

from message_schema import Updater

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


def generate_payload(text: str):
    return {
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
            "text": text
        }
    }


async def init_stages():
    # Инициализируем соединие с mc
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

    state = {
        0: hello_message,
        1: get_vacancy,
        2: add_vacancy_to_favorites,
        3: history_viewed_vacancy,
        4: viewed_history_already_cleaned,
        5: add_vacancy_to_history,
        6: show_favor_vacancy,
        7: return_to_init_state,
        8: uncover_vacancy_info,
        9: get_extend_vacancy,
        10: nothing_found
    }

    tokenizer = QueryBuilder(out_clean='str', out_token='list')

    train_data: dict = {
        "Следующая": 1,
        "В избранное": 2,
        "Очистить": 3,
        "Очистил": 4,
        "Добавил": 5,
        "Избранное": 6,
        "В начало": 7,
        "Раскрыть": 8,
        "Расширенный": 9
    }

    model = Model()

    model.fit(train_data)

    system = Systems(mc=global_cache,
                     pg=pg,
                     local_cache=local_cache,
                     tokenizer=tokenizer,
                     model=model)

    stage = Stages(state, system)

    return stage, memcached, pg


class TestInternalSystem(asynctest.TestCase):

    async def test_node_with_timeout(self):
        stage, memcached, pg = await init_stages()

        memcached.flush_all()
        states = ["hello", "python", "Cледующая"]

        for text in states:
            data = generate_payload(text)

            message = Updater(**data)

            # засыпаем чтобы вернуться в первоначальный стейн
            if text == "Cледующая":
                sleep(cfg.app.constants.timeout_for_chat + 2)
            state_number = await stage.next(message)

            if text == "hello":
                log.debug("checking a positive thread when the user follows all the recommendations")
                log.debug("phrase check - hello")
                self.assertEqual(state_number, 0)
            elif text == "python":
                log.debug("phrase check - python")
                log.debug("we remain in the same state, but go through all the recommendations")
                self.assertEqual(state_number, 1)
            elif text == "Cледующая":
                log.debug("phrase check - yes")
                log.debug("we remain in the same state, but go through all the recommendations, but timeout")
                self.assertEqual(state_number, 0)
        memcached.close()
        pg.pool.close()

    async def test_positive_node_with_old_user(self):
        sleep(cfg.app.constants.timeout_for_chat + 2)

        stage, memcached, pg = await init_stages()

        states = ["Привет", "python", "Следующая", "Избранное"]

        for text in states:
            data = generate_payload(text)

            message = Updater(**data)

            state_number = await stage.next(message)
            if text == "Привет":
                log.debug("checking a positive thread when the user follows all the recommendations")
                log.debug("phrase check - hello")
                self.assertEqual(state_number, 0)
            elif text == "python":
                log.debug("phrase check - python")
                log.debug("we remain in the same state, but go through all the recommendations")
                self.assertEqual(state_number, 1)
            elif text == "Следующая":
                log.debug("phrase check - yes")
                log.debug(
                    "we answer yes to the question continue to show the recommendations that are stored in the cache")
                self.assertEqual(state_number, 1)
            elif text == "Избранное":
                log.debug("phrase check - избранное")
                log.debug("we answer the question no and reset the user state")
                self.assertEqual(state_number, 6)

        memcached.close()
        pg.pool.close()
