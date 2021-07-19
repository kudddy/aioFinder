from sqlalchemy import select, func, desc, or_, Table

from plugins.pg.tables import index_map, cache_index, vacancy_content, viewed_vacancy
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
    query = select(
        [search_result, vacancy_content.c.id, vacancy_content.c.title, vacancy_content.c.header]).select_from(
        j).order_by(
        desc(search_result.c.counter)).limit(cfg.app.constants.number_of_recs)

    return query


def main_search_query(text: list):
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
    done_search_query = select(
        [search_result, vacancy_content.c.id, vacancy_content.c.title, vacancy_content.c.header]).select_from(
        j).alias("done_search_query")

    return done_search_query


def sorting_by_viewed_vacancies(done_search_query: Table):
    j = done_search_query.outerjoin(viewed_vacancy, viewed_vacancy.c.vacancy_id == done_search_query.c.id)

    query_with_filter = select([done_search_query]).select_from(j). \
        where(viewed_vacancy.c.vacancy_id == None).order_by(
        desc(done_search_query.c.counter)).limit(cfg.app.constants.number_of_recs)

    return query_with_filter
