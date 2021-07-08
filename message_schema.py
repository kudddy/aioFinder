from typing import List, Dict, Union
from pydantic import BaseModel, Field

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


class From(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str or None = None
    language_code: str = None


class Chat(BaseModel):
    id: int
    first_name: str
    username: str or None = None
    type: str


class InlineKeyboard(BaseModel):
    text: str
    callback_data: str


class ReplyMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboard]]


class Message(BaseModel):
    message_id: int
    frm: From = Field(..., alias='from')
    chat: Chat
    date: int
    edit_date: int = None
    text: str
    reply_markup: ReplyMarkup = None


class CallbackQuery(BaseModel):
    id: str
    frm: From = Field(..., alias='from')
    message: Message
    chat_instance: str
    data: str


class Updater(BaseModel):
    update_id: int
    message: Message = None
    callback_query: CallbackQuery = None


data_for_callback = {
    "update_id": 632560344,
    "callback_query": {
        "id": "349750407818784147",
        "from": {
            "id": 81432612,
            "is_bot": False,
            "first_name": "Kirill",
            "username": "kkkkk_kkk_kkkkk",
            "language_code": "ru"
        },
        "message": {
            "message_id": 874,
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
            "date": 1600692962,
            "edit_date": 1600693642,
            "text": "печень",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "лола",
                            "callback_data": "A1"
                        }
                    ]
                ]
            }
        },
        "chat_instance": "4891727470677092353",
        "data": "A1"
    }
}

callback = {
    "update_id": 531126222,
    "callback_query": {
        "id": "349750408637655340",
        "from": {
            "id": 81432612,
            "is_bot": False,
            "first_name": "Kirill",
            "username": "kkkkk_kkk_kkkkk",
            "language_code": "ru"
        },
        "message": {
            "message_id": 2784,
            "from": {
                "id": 888186754,
                "is_bot": True,
                "first_name": "Night2DayChecker",
                "username": "big5_test_bot"
            },
            "chat": {
                "id": 81432612,
                "first_name": "Kirill",
                "username": "kkkkk_kkk_kkkkk",
                "type": "private"
            },
            "date": 1625762049,
            "text": "Команда Industrial NLP в [Sber.AI](http://sber.ai/) находится в поиске **Ml**\nengineera, готового развивать экспертизу методов NLP и реализовывать проекты с\nих помощью. \nВ задачи команды входит научная работа по развитию направления, а также\nпрототипирование и внедрение в промышленное применение различных решений на\nоснове NLP.\n\nЗадачи, которые придется решать, позволят коснуться всех аспектов работы с\nязыковыми моделями, включая ruGPT-3, в том числе использование в продакшене. \nЗначимым аспектом работы также будет подготовка научных публикаций и\nвыступления на конференциях, вплоть до крупнейших международных мероприятий. \n \nНа данный момент мы ведем разработки по нескольким направлениям: цифровые\nассистенты руководителя (различные модели суммаризации, анализа когнитивных\nискажений, генерация ответов на e-mails и проч.), машинный перевод и RnD в\nобласти PLP - Programming Language Processing - создание мультилингвальных\nтрансформеров для перевода кода с одного языка программирования на другой. В\nдальнейшем - задачи генерации кода. \n\n\n **Требования к кандидату:**\n\n * Знания и опыт в области Data Science, опыт работы в данной сфере от 2х лет;\n * Понимание текущего состояния области NLP, хорошо знаете и умеете пользоваться классическими подходами, изучаете последние исследования по теме;\n * Понимание принципов работы алгоритмов машинного обучения (линейная регрессия, логистическая регрессия, деревья решений, случайный лес, градиентный бустинг) и глубокого обучения (RNN, CNN, LSTM, Autoencoder), знание метрик для оценки качества;\n * Хорошее знание Python и библиотек для анализа данных (Pandas, NumPy, SciPy, Scikit-learn, Matplotlib), практический опыт применения baseline NLP стека (nltk, spacy, gensim, pymorphy2, glove, fasttext и т.д.);\n * Опыт применения GloVe, ELMo, RNN, CNN, Transformer, BERT и понимание архитектуры этих сетей;\n * Знание хотя бы одного из Deep Learning фреймворков: Tensorflow, PyTorch;\n * Опыт решения практических NLP-задач для русского языка (NER, Text Classification, Summarization, Topic Modeling, Question Answering);\n * Опыт работы с Hadoop, Hive, Spark;\n * Большим плюсом будет широкий кругозор в IT за рамками машинного обучения, например: базовые знания архитектуры Web-сервисов (REST API, микросервисы, gRPC), знание сетевых библиотек (Flask, Django, Fastapi, SQLAlchemy или аналогичные);\n * Также значительным плюсом будет знание комбинаторики и методов дискретной оптимизации.\n\n\n\n **Наши условия:**\n\n * Современный IT-офис вблизи м. Кутузовская, с фитнес залом, бесплатным подземным паркингом;\n * Позитивная и заряженная команда профессионалов;\n * Интересные, сложные, амбициозные задачи;\n * Многообразие проектов в интересной команде;\n * Возможность профильного обучения за счет компании;\n * Стабильная, конкурентная «белая» заработная плата (оклад + достойные премии);\n * Льготные условия по ипотеке и кредитам Сбера;\n * ДМС, социальные гарантии, корпоративные мероприятия.",
            "entities": [
                {
                    "offset": 26,
                    "length": 7,
                    "type": "url"
                },
                {
                    "offset": 35,
                    "length": 15,
                    "type": "url"
                }
            ],
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "Да",
                            "callback_data": "A1"
                        },
                        {
                            "text": "Нет",
                            "callback_data": "A1"
                        }
                    ]
                ]
            }
        },
        "chat_instance": "-5135792011174378514",
        "data": "A1"
    }
}

