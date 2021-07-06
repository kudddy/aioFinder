# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import sys
from collections import defaultdict, Iterable

from aiohttp_requests import requests


async def send_message(url: str,
                       chat_id: int,
                       text: str,
                       parse_mode: str = None,
                       buttons: list or None = None,
                       inline_keyboard: list or None = None,
                       one_time_keyboard: bool = True,
                       resize_keyboard: bool = True,
                       remove_keyboard: bool = False):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "remove_keyboard": remove_keyboard
        }
    }

    if parse_mode:
        payload.update({"parse_mode": parse_mode})

    if buttons:
        # TODO hardcode
        keyboards = [[{"text": text}] for text in buttons]
        payload["reply_markup"].update({
            "keyboard": keyboards,
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard
        })

    if inline_keyboard:
        payload["reply_markup"].update({"inline_keyboard": inline_keyboard})

    headers = {
        "Content-Type": "application/json",
    }

    await requests.get(url, headers=headers, data=payload, ssl=False)


async def edit_message_text(url: str,
                            text: str,
                            chat_id: int or str = None,
                            message_id: int = None,
                            inline_message_id: str = None,
                            parse_mode: str = None,
                            entities: str = None,
                            disable_web_page_preview: bool = None,
                            reply_markup=None
                            ):
    payload = {
        "text": text
    }
    if chat_id:
        payload.update({"chat_id": chat_id})
    if message_id:
        payload.update({"message_id": message_id})

    headers = {
        "Content-Type": "application/json",
    }

    payload = json.dumps(payload)

    await requests.get(url, headers=headers, data=payload, ssl=False)


# class GetVac:
#     def __init__(self, vacs_filename):
#         self.vacs = pcl.get_pickle_file(vacs_filename)
#
#     def get_vac_by_id(self, key: int):
#         if key in self.vacs.keys():
#             return self.vacs[key]
#         else:
#             return False
#
#     def update_cache(self, new_cache):
#         self.vacs = new_cache


############## ф-ции общего назначения

class Coder:
    @staticmethod
    def encode(obj: object):
        return json.dumps(obj).encode()

    @staticmethod
    def decode(byte: bytes):
        return json.loads(byte.decode())


def split_dict_equally(input_dict, chunks=2):
    """
    Разделение словаря на n частей. Возвращает лист из словарей.
    Аrgs:
        type(dict) - input_dict : словарь с любым типом данных
        type(int) - chunks : размер выходного списка
    Returns:
        type(list) - return_list : список с словарями
    """
    # prep with empty dicts
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for k, v in input_dict.items():
        return_list[idx][k] = v
        if idx < chunks - 1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list


def func(*dicts):
    """
    Объединяет словари по ключа. Работает только со строками
    Аrgs:
        type(dict) - input_dict : словари
    Returns:
        type(list) - return_list : список с словарями
    """
    keys = set().union(*dicts)
    return {k: " ".join(dic.get(k, '') for dic in dicts) for k in keys}


def check_updates(recs_new, recs_old):
    """
    В случае если старые и новые рекомендации разные,то возвращаем True, если же одинаковые то
    False
    Аrgs:
        type(list) - recs_new : список с новыми рекомендациями
        type(list) - recs_old : строка c sf_id
    Returns:
        type(list) - jc : список с актуальными jc
    """
    len_intersect = len(set(recs_old).intersection(set(recs_new)))

    len_old_rec = len(recs_old)

    if len_intersect == len_old_rec and recs_old == recs_new:
        return False
    else:
        return True


def get_score(recs_new):
    """
    Ф-ция возвращает искуственно созданных скор для рекомендаций в зависимости от кол-ва новых рекомендаций
    Аrgs:
        type(list) - recs_new : список с новыми рекомендациями
    Returns:
        type(list) - score : список со скором
    """
    len_recs = len(recs_new)
    min_trash = 0.6
    max_trash = 0.95
    score = []
    error = 0
    for i in range(len(recs_new)):
        error += (max_trash - min_trash) / len_recs
        score.append(str(max_trash - error))
    return score


def group_by_value(dct):
    """
    Группируем ключ по значениям
    Аrgs:
        type(dict) - input_dict : словарь с любым типом данных
        type(int) - chunks : размер выходного списка
    Returns:
        type(list) - return_list : список с словарями
    """
    v = {}
    for key, value in sorted(dct.items()):
        v.setdefault(value, []).append(key)
    return v


def group_tuples_by_key(tuples):
    """
    Ф-ция возвращает сгруппированный по ключу словарь
    Аrgs:
        type(list((key,val),(key,val))) - tuples : список с кортежами
    Returns:
        type(dict) - score : сгруппированный по ключу словарь
    """
    d = defaultdict(list)
    for k, *v in tuples:
        d[k].append(v[0])
    b = list(d.items())
    return dict(b)


def add_list(main_list, new_list):
    """
    Ф-ция добавляет в начала списка main_list список new_list
    Аrgs:
        type(list) - main_list : основной список с элементами
        type(list) - bad_list : список элементов, которые нужно удалить из основного списка
    Returns:
        type(list) - new_list : новый список
    """
    return new_list + main_list


def diff_no_mutation(main_list, bad_list):
    """
    Ф-ция возвращает список элементов main_list которых нет в bad_list
    Аrgs:
        type(list) - main_list : основной список с элементами
        type(list) - bad_list : список элементов, которые нужно удалить из основного списка
    Returns:
        type(list) - clean_list : очищенный список
    """
    clean_list = [x for x in main_list if x not in bad_list]
    return clean_list


def drop_dublicates_list(seq):
    """
    Удаляем дубликаты из списка
    Аrgs:
        type(list) - seq : основной список с элементами
    Returns:
        type(list) - clean_list : список без дубликатов
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def chunks(array, chunk_size):
    """
    Ф-ция возвращает сгруппированный по ключу словарь. Ф-цию нужно обернуть в list()
    Аrgs:
        type(list)- array : список
        type(int) - chunk_size : коэф от которого зависит какой размер батча
    Returns:
        n/a
    """
    for i in range(0, len(array), chunk_size):
        yield array[i:i + chunk_size]


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from (flatten(x))
        else:
            yield x


def structure_normalization(d: list) -> dict:
    """
    Нормализация структуры данных, которая приходит из JobApi
    :param d:
    :return:
    """
    local_dict = {}
    for k in d:
        local_dict.update({k['id']: k})
    return local_dict


# class GetVac:
#     def __init__(self, vacs_filename):
#         self.vacs = pcl.get_pickle_file(vacs_filename)
#
#     def get_vac_by_id(self, key: int):
#         if key in self.vacs.keys():
#             return self.vacs[key]
#         else:
#             return False
#
#     def update_cache(self, new_cache):
#         self.vacs = new_cache


def remove_html_in_dict(text):
    html_pattern = re.compile('<.*?>')
    title_pattern = re.compile(r'([a-zа-я](?=[A-ZА-Я])|[A-ZА-Я](?=[A-ZА-Я][a-zа-я]))')

    val = title_pattern.sub(r'\1 ', html_pattern.sub(r'', text).replace('\xa0', ' '))
    text = re.sub(r'&[\w]*;', ' ', val).strip()
    return text


def get_clean_text_str(text_vacs: dict) -> str:
    """
    Ф-ция необходима для процедуры токенизации. Преобразует данные из словаря в единую строку
    :param text_vacs: словарь с описанием вакансии
    :return: единая строка содержащая в себе поля
    """
    if 'title' in text_vacs.keys():
        title = remove_html_in_dict(text_vacs['title'])
    else:
        title = 'fail'

    # обязанности
    if 'duties' in text_vacs.keys():
        duties_text = remove_html_in_dict(text_vacs['duties'])
    else:
        duties_text = 'fail'

    # условия
    if 'conditions' in text_vacs.keys():
        # conditions_text = remove_html_in_dict(text_vacs['conditions'])
        conditions_text = 'fail'
    else:
        conditions_text = 'fail'

    return title + ' ' + duties_text


def model_result(input_vector: dict, token: str, url: str) -> list:
    url = url + 'get_recs'

    data = {
        'token': token,
        'vector': input_vector
    }
    result = get_response(url, data)
    if result['status'] == 'ok':
        result = result['result']
    else:
        result = []

    return result


def search_result(text: str, token: str, url: str) -> list:
    url = url + 'search'

    data = {
        'token': token,
        'string': text
    }
    result = get_response(url, data)
    if result['status'] == 'ok':
        result = result['result']
    else:
        result = []

    return result


def get_response(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    payload = json.dumps(data)
    r = requests.post(url, data=payload, headers=headers)
    result = r.json()
    return result


def get_nearest_vac(url: str, city: str):
    data = {
        "token": "shdfksdhflkdsfh",
        "data": city,
        "get_vac": True
    }
    nearest_vac = get_response(url, data)

    status = nearest_vac['status']

    if status:
        return nearest_vac['data']
    else:
        return -1
