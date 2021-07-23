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
    callback_data: str or None = None
    url: str or None = None


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

    def its_callback(self):
        if self.callback_query:
            return True
        else:
            return False

    def get_message_id(self):

        if self.its_callback():
            message_id = self.callback_query.message.message_id
        else:
            message_id = self.message.message_id

        return message_id

    def get_chat_id(self):
        if self.its_callback():
            chat_id = self.callback_query.message.chat.id
        else:
            chat_id = self.message.chat.id

        return chat_id

    def get_text(self):
        if self.its_callback():
            text = self.callback_query.data
        else:
            text = self.message.text

        return text

    def get_user_id(self):
        if self.its_callback():
            user_id = self.callback_query.message.frm.id
        else:
            user_id = self.message.frm.id
        return user_id

    def get_username(self):
        if self.its_callback():
            username = self.callback_query.message.frm.username
        else:
            username = self.message.frm.username
        return username


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

data = {
    "update_id": 531126412,
    "callback_query": {
        "id": "349750407619198040",
        "from": {
            "id": 81432612,
            "is_bot": False,
            "first_name": "Kirill",
            "username": "kkkkk_kkk_kkkkk",
            "language_code": "ru"
        },
        "message": {
            "message_id": 3018,
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
            "date": 1626105119,
            "text": "kkk",
            "entities": [
                {
                    "offset": 35,
                    "length": 7,
                    "type": "url"
                },
                {
                    "offset": 82,
                    "length": 7,
                    "type": "url"
                },
                {
                    "offset": 91,
                    "length": 15,
                    "type": "url"
                }
            ],
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "Да",
                            "callback_data": "Да"
                        },
                        {
                            "text": "Нет",
                            "callback_data": "Нет"
                        }
                    ],
                    [
                        {
                            "text": "Описание и отклик",
                            "url": "https://my.sbertalents.ru/#/job-requisition/2110375"
                        }
                    ]
                ]
            }
        },
        "chat_instance": "-5135792011174378514",
        "data": "Да"
    }
}

m = Updater(**data)

response_from_tlg = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message text is empty"
}