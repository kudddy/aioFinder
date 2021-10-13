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

    memcached.flush_all()

    return stage, memcached, pg


class TestInternalSystem(asynctest.TestCase):

    # async def test_node_with_timeout(self):
    #     stage, memcached, pg = await init_stages()
    #
    #     log.debug("checking a positive thread when the user follows all the recommendations")
    #     log.debug("phrase check - hello")
    #
    #     data = {
    #         "update_id": 243475549,
    #         "message": {
    #             "message_id": 9450,
    #             "from": {
    #                 "id": 81432612,
    #                 "is_bot": False,
    #                 "first_name": "Kirill",
    #                 "username": "kkkkk_kkk_kkkkk",
    #                 "language_code": "ru"
    #             },
    #             "chat": {
    #                 "id": 81432612,
    #                 "first_name": "Kirill",
    #                 "username": "kkkkk_kkk_kkkkk",
    #                 "type": "private"
    #             },
    #             "date": 1589404439,
    #             "text": "hello"
    #         }
    #     }
    #
    #     message = Updater(**data)
    #
    #     state_number = await stage.next(message)
    #
    #     self.assertEqual(state_number, 0)
    #
    #     log.debug("phrase check - python")
    #     log.debug("we remain in the same state, but go through all the recommendations")
    #
    #     data = {
    #         "update_id": 243475549,
    #         "message": {
    #             "message_id": 9450,
    #             "from": {
    #                 "id": 81432612,
    #                 "is_bot": False,
    #                 "first_name": "Kirill",
    #                 "username": "kkkkk_kkk_kkkkk",
    #                 "language_code": "ru"
    #             },
    #             "chat": {
    #                 "id": 81432612,
    #                 "first_name": "Kirill",
    #                 "username": "kkkkk_kkk_kkkkk",
    #                 "type": "private"
    #             },
    #             "date": 1589404439,
    #             "text": "python"
    #         }
    #     }
    #
    #     message = Updater(**data)
    #
    #     state_number = await stage.next(message)
    #
    #     self.assertEqual(state_number, 1)
    #
    #     log.debug("phrase check - yes")
    #     log.debug("we remain in the same state, but go through all the recommendations, but timeout")
    #
    #     data = {
    #         "update_id": 243475549,
    #         "message": {
    #             "message_id": 9450,
    #             "from": {
    #                 "id": 81432612,
    #                 "is_bot": False,
    #                 "first_name": "Kirill",
    #                 "username": "kkkkk_kkk_kkkkk",
    #                 "language_code": "ru"
    #             },
    #             "chat": {
    #                 "id": 81432612,
    #                 "first_name": "Kirill",
    #                 "username": "kkkkk_kkk_kkkkk",
    #                 "type": "private"
    #             },
    #             "date": 1589404439,
    #             "text": "python"
    #         }
    #     }
    #
    #     message = Updater(**data)
    #
    #     sleep(cfg.app.constants.timeout_for_chat + 2)
    #
    #     state_number = await stage.next(message)
    #
    #     self.assertEqual(state_number, 0)
    #
    #     memcached.flush_all()
    #
    #     sleep(cfg.app.constants.timeout_for_chat + 2)
    #
    #     memcached.close()
    #     pg.pool.close()

    async def test_positive_node_with_old_user(self):
        stage, memcached, pg = await init_stages()

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

        self.assertEqual(state_number, 0)

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
                "text": "Следующая"
            }
        }

        message = Updater(**data)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 1)

        log.debug("phrase check - no")
        log.debug("we answer the question no and reset the user state")

        data = {
            "update_id": 632563159,
            "callback_query": {
                "id": "349750407540136990",
                "from": {
                    "id": 81432612,
                    "is_bot": False,
                    "first_name": "Kirill",
                    "username": "kkkkk_kkk_kkkkk",
                    "language_code": "ru"
                },
                "message": {
                    "message_id": 3573,
                    "from": {
                        "id": 1238618041,
                        "is_bot": True,
                        "first_name": "work_founder",
                        "username": "work_founder_bot"
                    },
                    "chat": {
                        "id": 81432612,
                        "first_name": "Kirill",
                        "username": "kkkkk_kkk_kkkkk",
                        "type": "private"
                    },
                    "date": 1634143895,
                    "text": "💥 Название позиции: Scala-разработчик (SberDs)\n💥 Описание: Мы - Трайб Управление модельного риска. Мы разрабатываем новую инновационную\nПлатформу Sberbank.DS Ecosystem. Это линейка продуктов, решающая задачи\nСбербанка по ускоренной разработке, валидации и мониторингу AI моделей.\nСтратегически планируется продвижение Платформы (коробочный продукт, облачные\nсервисы) на российский и международный рынок.\n\n  \nРазвитие Платформы соответствует мировым трендам «демократизации AI», когда\nразработка модели превращается в задачу, доступную любому пользователю че...\n\nПоказать еще❓",
                    "reply_markup": {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "Полное описание и отклик",
                                    "url": "https://my.sbertalents.ru/#/job-requisition/1961048"
                                },
                                {
                                    "text": "Расширенный профиль",
                                    "callback_data": "Расширенный"
                                }
                            ],
                            [
                                {
                                    "text": "Назад к выбору",
                                    "callback_data": "В начало"
                                },
                                {
                                    "text": "Следующая",
                                    "callback_data": "Следующая"
                                }
                            ],
                            [
                                {
                                    "text": "В избранное",
                                    "callback_data": "В избранное"
                                },
                                {
                                    "text": "Показать избранные",
                                    "callback_data": "Избранное"
                                }
                            ],
                            [
                                {
                                    "text": "Очистить историю просмотров",
                                    "callback_data": "Очистить"
                                }
                            ]
                        ]
                    }
                },
                "chat_instance": "4891727470677092353",
                "data": "Избранное"
            }
        }

        message = Updater(**data)

        state_number = await stage.next(message)

        self.assertEqual(state_number, 6)

        memcached.close()
        pg.pool.close()
