from typing import List, Dict, Union
from pydantic import BaseModel, Field


# val['cache_vacancy_result'] = arr
# val['cache_iter'] = step
class CacheStructure(BaseModel):
    # шаг в сценарии
    step: int
    # закешированные значения по вакансиями
    cache_vacancy_result: list
    # текущая позиция пользователя в списке вакансий
    cache_iter: int
