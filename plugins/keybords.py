from random import choice

emoticons = ['🔥', '❤', '️🤡', '🤮', '💋', '👅', '👀', '🐒', '🍒', '🥟', '🍤']


def back_to_selection():
    return {

        "text": "Назад к выбору",

        "callback_data": "В начало"

    }


def next_item():
    return {

        "text": "Следующая",

        "callback_data": "Следующая"

    }


def to_favor():
    return {

        "text": "В избранное",

        "callback_data": "В избранное"

    }


def show_favor():
    return {

        "text": "Показать избранные",

        "callback_data": "Избранное"
    }


def clean_history():
    return {

        "text": "Очистить историю просмотров",

        "callback_data": "Очистить"
    }


def add_item(double_click: bool = False):
    if double_click:

        return {

            "text": choice(emoticons),

            "callback_data": "Добавил"

        }

    else:

        return {

            "text": "Добавил 👍",

            "callback_data": "Добавил"

        }


def desk_and_response(url: str):
    return {
        "text": "Описание и отклик",
        "url": url,
        "callback_data": ""
    }


def double_click_to_add_item():
    return {

        "text": choice(emoticons),

        "callback_data": "Добавил"

    }


def click_to_clean_items(double_click: bool):
    if double_click:
        return {
            "text": choice(emoticons),
            "callback_data": "Очистил"
        }
    else:
        return {
            "text": "Очистил 👍",
            "callback_data": "Очистил"
        }


def get_reveal_button(url: str, extend_profile: bool):
    if extend_profile:
        return [
            {

                "text": "Полное описание и отклик",

                "callback_data": "",

                "url": url,

            },
            {

                "text": "Расширенный профиль",

                "callback_data": "Расширенный"

            }

        ]
    else:
        return [
            {

                "text": "Полное описание и отклик",

                "callback_data": "",

                "url": url,

            }
        ]


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


def generate_pagination_keyboard(url: str,
                                 extend_profile: bool,
                                 reveal_text: bool = True,
                                 ):
    """
    Генерация клавиатуры для самого первого экрана
    :param extend_profile:  показывать расширенный профиль по локации или нет
    :param reveal_text: выводить кнопку  "Раскрыть" или нет
    :param url: ссылка на вакансию
    :return:
    """
    inline_keyboard_for_pagination = [
        [
            back_to_selection(),
            next_item()
        ],
        [
            to_favor(),
            show_favor()
        ],
        [
            clean_history()
        ]

    ]

    if reveal_text:
        inline_keyboard_for_pagination.insert(0, get_reveal_button(url, extend_profile))
    return inline_keyboard_for_pagination


def generate_check_box_keyboard(url: str,
                                reveal_text: bool = True,
                                extend_profile: bool = False):
    """
    Функция генерации кнопок в момент нажатия на кнопку "Добавить в избанное"
    :param extend_profile: Показывать расширенный профиль или нет
    :param reveal_text: выводить кнопку  "Раскрыть" или нет
    :param url: ссылка на вакансию
    :return: готовые массив с кнопками
    """
    inline_keyboard_for_check_box = [
        [
            back_to_selection(),
            next_item()
        ],
        [
            add_item(),
            show_favor()
        ],
        [
            clean_history()
        ],
        [
            get_reveal_button(url, extend_profile)[0]
        ]
    ]
    # if reveal_text:
    #     inline_keyboard_for_check_box.insert(0, get_reveal_button(url, extend_profile))
    return inline_keyboard_for_check_box


def generate_emo_keyboard(url: str,
                          reveal_text: bool = True,
                          extend_profile: bool = False):
    """
    Функция генерирует кнопки в момент, когда пользователь повторно нажимает на "Добавить в избранное"
    :param extend_profile: Показывать расширенный профиль или нет
    :param reveal_text:
    :param url:
    :return:
    """
    inline_keyboard_for_emo = [
        [
            back_to_selection(),
            next_item()
        ],
        [
            add_item(double_click=True),
            show_favor(),
        ],
        [
            clean_history()
        ]
    ]

    if reveal_text:
        inline_keyboard_for_emo.insert(0, get_reveal_button(url, extend_profile))
    return inline_keyboard_for_emo


def generate_check_box_for_clean(url: str,
                                 double_click: bool = False,
                                 reveal_text: bool = True,
                                 extend_profile: bool = True):
    """
    Фукция генерирует кнопки в момент нажатия на кнопку "Очистить"
    :param extend_profile: Показывать расширенный профиль или нет
    :param reveal_text:
    :param url:
    :param double_click:
    :return:
    """

    inline_keyboard_for_pagination = [
        [
            back_to_selection(),
            next_item()
        ],
        [
            to_favor(),
            show_favor()
        ],
        [
            click_to_clean_items(double_click=double_click)
        ]
    ]

    if reveal_text:
        inline_keyboard_for_pagination.insert(0, get_reveal_button(url, extend_profile))

    return inline_keyboard_for_pagination


def generate_keyboard_for_likes(url: str,
                                reveal_text: bool = True,
                                extend_profile: bool = False):
    """
    Кнопка для показала избранных позиций
    :param extend_profile: Показывать расширенный профиль или нет
    :param reveal_text:
    :param url:
    :return:
    """

    inline_keyboard_for_likes = [
        [
            back_to_selection(),
            next_item()
        ]
    ]
    if reveal_text:
        inline_keyboard_for_likes.insert(0, get_reveal_button(url, extend_profile))
    return inline_keyboard_for_likes
