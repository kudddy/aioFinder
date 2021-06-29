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

