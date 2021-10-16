from plugins.classifier import Model
from plugins.callback import hello_message, get_vacancy, \
    add_vacancy_to_favorites, history_viewed_vacancy, \
    viewed_history_already_cleaned, add_vacancy_to_history, \
    show_favor_vacancy, return_to_init_state, \
    uncover_vacancy_info, get_extend_vacancy, nothing_found


train_data: dict = {
    "Следующая": 1,
    "В избранное": 2,
    "Очистить": 3,
    "Очистил": 4,
    "Добавил": 5,
    "Избранное": 6,
    "В начало": 0,
    "Раскрыть": 8,
    "Расширенный": 9
}
# коллбэк функции
model = Model()

model.fit(train_data)

state = {
    0: hello_message,
    1: get_vacancy,
    2: add_vacancy_to_favorites,
    3: history_viewed_vacancy,
    4: viewed_history_already_cleaned,
    5: add_vacancy_to_history,
    6: show_favor_vacancy,
    7: return_to_init_state,
    8: uncover_vacancy_info,
    9: get_extend_vacancy,
    10: nothing_found
}
