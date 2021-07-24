from random import choice

emoticons = ['🔥', '❤', '️🤡', '🤮', '💋', '👅', '👀', '🐒', '🍒', '🥟', '🍤']

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


def generate_pagination_keyboard(url: str):
    inline_keyboard_for_pagination = [
        [
            {
                "text": "Следующая",
                "callback_data": "Следующая"
            },
            {
                "text": "Назад к выбору",
                "callback_data": "В начало"

            },
        ],
        [
            {
                "text": "Добавить в избранное",
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
        [
            {
                "text": "Описание и отклик",
                "url": url,
                "callback_data": ""
            }
        ]
    ]
    return inline_keyboard_for_pagination


def generate_check_box_keyboard(url: str):
    inline_keyboard_for_check_box = [
        [
            {
                "text": "Следующая",
                "callback_data": "Следующая"
            },
            {
                "text": "Назад к выбору",
                "callback_data": "В начало"

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
    return inline_keyboard_for_check_box


def generate_emo_keyboard(url: str):
    inline_keyboard_for_emo = [
        [
            {
                "text": "Следующая",
                "callback_data": "Следующая"
            },
            {
                "text": "Назад к выбору",
                "callback_data": "В начало"

            },
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
        [
            {
                "text": "Описание и отклик",
                "url": url,
                "callback_data": ""
            }
        ]
    ]
    return inline_keyboard_for_emo


def generate_check_box_for_clean(url: str, double_click: bool = False):
    if double_click:
        inline_keyboard_for_pagination = [
            [
                {
                    "text": "Следующая",
                    "callback_data": "Следующая"
                },
                {
                    "text": "Назад к выбору",
                    "callback_data": "В начало"

                },
            ],
            [
                {
                    "text": "Добавить в избранное",
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
            [
                {
                    "text": "Описание и отклик",
                    "url": url,
                    "callback_data": ""
                }
            ]
        ]
    else:
        inline_keyboard_for_pagination = [
            [
                {
                    "text": "Следующая",
                    "callback_data": "Следующая"
                },
                {
                    "text": "Назад к выбору",
                    "callback_data": "В начало"

                },
            ],
            [
                {
                    "text": "Добавить в избранное",
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
            [
                {
                    "text": "Описание и отклик",
                    "url": url,
                    "callback_data": ""
                }
            ]
        ]

    return inline_keyboard_for_pagination


def generate_keyboard_for_likes(url):
    inline_keyboard_for_likes = [
        [
            {
                "text": "Следующая",
                "callback_data": "Следующая"
            },
            {
                "text": "Назад к выбору",
                "callback_data": "В начало"

            },
        ],
        [
            {
                "text": "Описание и отклик",
                "url": url,
                "callback_data": ""
            }
        ]
    ]
    return inline_keyboard_for_likes
