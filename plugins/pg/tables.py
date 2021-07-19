from enum import Enum, unique

from sqlalchemy import (
    Column, Date, Enum as PgEnum, ForeignKey, ForeignKeyConstraint, Integer,
    MetaData, String, Table
)

from sqlalchemy.types import UserDefinedType

# SQLAlchemy рекомендует использовать единый формат для генерации названий для
# индексов и внешних ключей.
# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


# добавлена поддерка типа CUBE
class CUBE(UserDefinedType):
    def get_col_spec(self, **kw):
        return "CUBE"


vacancy_content = Table(
    'vacancy_content',
    metadata,
    Column('id', Integer),
    Column('title', String),
    Column('footer', String),
    Column('header', String),
    Column('requirements', String),
    Column('duties', String),
    Column('conditions', String),
    Column('date', Date),
    Column('locality', Integer),
    Column('region', Integer),
    Column('company', Integer)
)

index_map = Table(
    'index_map',
    metadata,
    Column('extended_index', String),
    Column('original_index', String)
)

cache_index = Table(
    'cache_index',
    metadata,
    Column('original_index', String),
    Column('vacancy_id', Integer)

)

user_enter = Table(
    'user_enter',
    metadata,
    Column('user_id', Integer),
    Column('chat_id', Integer),
    Column('date', Date)
)

likes_info = Table(
    'likes_info',
    metadata,
    Column('user_id', Integer),
    Column('chat_id', Integer),
    Column('date', Date),
    Column('vacancy_id', Integer)
)

viewed_vacancy = Table(
    'viewed_vacancy',
    metadata,
    Column('user_id', Integer),
    Column('chat_id', Integer),
    Column('date', Date),
    Column('vacancy_id', Integer)

)