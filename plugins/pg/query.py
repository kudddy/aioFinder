from sqlalchemy import select, func, desc, or_

from plugins.pg.tables import index_map, cache_index, vacancy_content
from plugins.config import cfg


def generate_search_query(text: list):

    tokens = [index_map.c.extended_index == x for x in text]
    times = select([index_map.c.original_index]). \
        where(or_(*tokens)). \
        alias("times")

    j = times.join(cache_index, times.c.original_index == cache_index.c.original_index)

    search_result = select([cache_index.c.vacancy_id, func.count(cache_index.c.vacancy_id).label('counter')]). \
        select_from(j). \
        group_by(cache_index.c.vacancy_id). \
        order_by(desc('counter')). \
        alias("search_result")

    j = search_result.join(vacancy_content, search_result.c.vacancy_id == vacancy_content.c.id)
    # TODO выгружаю слишком много данных, не помещается в кэш
    query = select([search_result, vacancy_content]).select_from(j).order_by(
        desc(search_result.c.counter)).limit(cfg.app.constants.number_of_recs)

    return query
