from random import choice

emoticons = ['🔥', '❤', '️🤡', '🤮', '💋', '👅', '👀', '🐒', '🍒', '🥟', '🍤']


# reveal_button = [
#     {
#         "text": "Раскрыть полностью?",
#         "callback_data": "Раскрыть"
#     }
# ]

def get_reveal_button(url: str):
    reveal_button = [
        {
            "text": "Полное описание и отклик",
            "callback_data": "",
            "url": url,

        }
    ]
    return reveal_button


inline_keyboard_for_hello = [
    [
        {
            "text": "JavaScript",
            "callback_data": "JavaScript"
        },
        {
            "text": "Python",
            "callback_data": "Python"

        },
    ],
    [
        {
            "text": "Java, Scala",
            "callback_data": "Java, Scala"
        },
        {
            "text": "C/C++, Assembler",
            "callback_data": "C/C++, Assembler"
        }
    ],
    [
        {
            "text": "PHP",
            "callback_data": "PHP"
        },
        {
            "text": ".NET",
            "callback_data": ".NET"
        },
        {
            "text": "QA",
            "callback_data": "QA"
        }
    ],
    [
        {
            "text": "DevOps",
            "callback_data": "DevOps"
        },
        {
            "text": "IOS",
            "callback_data": "IOS"
        },
        {
            "text": "Golang",
            "callback_data": "Golang"
        }
    ],
    [
        {
            "text": "Data Science",
            "callback_data": "DS, Data Science"
        },
        {
            "text": "Security",
            "callback_data": "Security, безопасность"
        },
    ],
    [
        {
            "text": "Analyst",
            "callback_data": "Analyst"
        },
        {
            "text": "Manager",
            "callback_data": "Manager"
        }
    ]

]


def generate_pagination_keyboard(url: str, reveal_text: bool = True):
    """
    Генерация клавиатуры для самого первого экрана
    :param reveal_text: выводить кнопку  "Раскрыть" или нет
    :param url: ссылка на вакансию
    :return:
    """
    inline_keyboard_for_pagination = [
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
        ],
        # [
        #     {
        #         "text": "Описание и отклик",
        #         "url": url,
        #         "callback_data": ""
        #     }
        # ]
    ]

    if reveal_text:
        inline_keyboard_for_pagination.insert(0, get_reveal_button(url))
    return inline_keyboard_for_pagination


def generate_check_box_keyboard(url: str, reveal_text: bool = True):
    """
    Функция генерации кнопок в момент нажатия на кнопку "Добавить в избанное"
    :param reveal_text: выводить кнопку  "Раскрыть" или нет
    :param url: ссылка на вакансию
    :return: готовые массив с кнопками
    """
    inline_keyboard_for_check_box = [
        [
            {
                "text": "Назад к выбору",
                "callback_data": "В начало"

            },
            {
                "text": "Следующая",
                "callback_data": "Следующая"
            },
        ],
        [
            {
                "text": "Добавил 👍",
                "callback_data": "Добавил"
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
        ],
        [
            {
                "text": "Описание и отклик",
                "url": url,
                "callback_data": ""
            }
        ]
    ]
    if reveal_text:
        inline_keyboard_for_check_box.insert(0, get_reveal_button(url))
    return inline_keyboard_for_check_box


def generate_emo_keyboard(url: str, reveal_text: bool = True):
    """
    Функция генерирует кнопки в момент, когда пользователь повторно нажимает на "Добавить в избранное"
    :param reveal_text:
    :param url:
    :return:
    """
    inline_keyboard_for_emo = [
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
                "text": choice(emoticons),
                "callback_data": "Добавил"
            },
            {
                "text": "Показать избранные",
                "callback_data": "Избранное"
            }
        ],
        [
            {
                "text": "Очистить историю просмотров",
                "callback_data": "Очистил"
            }
        ],
        # [
        #     {
        #         "text": "Описание и отклик",
        #         "url": url,
        #         "callback_data": ""
        #     }
        # ]
    ]

    if reveal_text:
        inline_keyboard_for_emo.insert(0, get_reveal_button(url))
    return inline_keyboard_for_emo


def generate_check_box_for_clean(url: str, double_click: bool = False, reveal_text: bool = True):
    """
    Фукция генерирует кнопки в момент нажатия на кнопку "Очистить"
    :param reveal_text:
    :param url:
    :param double_click:
    :return:
    """

    if double_click:
        inline_keyboard_for_pagination = [
            [
                {
                    "text": "Назад к выбору",
                    "callback_data": "В начало"

                },
                {
                    "text": "Следующая",
                    "callback_data": "Следующая"
                },
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
                    "text": choice(emoticons),
                    "callback_data": "Очистил"
                }
            ],
            # [
            #     {
            #         "text": "Описание и отклик",
            #         "url": url,
            #         "callback_data": ""
            #     }
            # ]
        ]
    else:
        inline_keyboard_for_pagination = [
            [
                {
                    "text": "Назад к выбору",
                    "callback_data": "В начало"

                },
                {
                    "text": "Следующая",
                    "callback_data": "Следующая"
                },
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
                    "text": "Очистил 👍",
                    "callback_data": "Очистил"
                }
            ],
            # [
            #     {
            #         "text": "Описание и отклик",
            #         "url": url,
            #         "callback_data": ""
            #     }
            # ]
        ]

    if reveal_text:
        inline_keyboard_for_pagination.insert(0, get_reveal_button(url))

    return inline_keyboard_for_pagination


def generate_keyboard_for_likes(url: str, reveal_text: bool = True):
    """
    Кнопка для показала избранных позиций
    :param reveal_text:
    :param url:
    :return:
    """

    inline_keyboard_for_likes = [
        [
            {
                "text": "Назад к выбору",
                "callback_data": "В начало"

            },
            {
                "text": "Следующая",
                "callback_data": "Следующая"
            },
        ],
        # [
        #     {
        #         "text": "Описание и отклик",
        #         "url": url,
        #         "callback_data": ""
        #     }
        # ]
    ]
    if reveal_text:
        inline_keyboard_for_likes.insert(0, get_reveal_button(url))
    return inline_keyboard_for_likes
