from message_schema import Updater
# from plugins.statemachine import LocalCacheForCallbackFunc
from plugins.cache import LocalCacheForCallbackFunc
from plugins.config import cfg
from plugins.helper import send_message
from plugins.helper import remove_html_in_dict

# from plugins.cache import mc

# # инициализируем класс с вакансиями
# vacs = GetVac(vacs_filename=vacs_filename)
# # инициализируем поисковой движок
# search = InversIndexSearch(url=url_fasttext, token=token_fastext)

# инициализируем класс с кэшем только для коллбэк ф-ций
# cache = LocalCacheForCallbackFunc()


async def hello_message(m: Updater, cache: LocalCacheForCallbackFunc):
    """
    Приветственное сообщение с просьбой указать навык
    :param cache:
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    if m.message:
        await cache.clean(m.message.chat.id)
    else:
        await cache.clean(m.callback_query.message.chat.id)

    text = "💥 Приветствую, я найду для тебя работу. Введите свой ключевой навык❗"
    await send_message(cfg.app.hosts.tlg.host,
                       m.message.chat.id,
                       text,
                       remove_keyboard=True)
    return 1


async def analyze_text_and_give_vacancy(m: Updater, cache: LocalCacheForCallbackFunc):
    """
    :param cache:
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    if m.message.text != 'Нет':
        if await cache.check(m.message.chat.id):
            await cache.next_step(m.message.chat.id)
        else:
            # возвращат id вакансии
            # result: list = search.search(m.message.text)
            result: list = [123, 456, 789]
            step = 0
            await cache.caching(m.message.chat.id,
                                step=step,
                                arr=result)
        vac_id = await cache.give_cache(m.message.chat.id)
        get_vac_by_id: dict = {
            123: {
                'content': {
                    'title': 'Пиздюк иваныч',
                    'header': 'В задачи вакансии входит ебать мозги'
                }
            },
            456: {
                'content': {
                    'title': 'Пиздюк иваныч',
                    'header': 'В задачи вакансии входит ебать мозги'
                }
            },
            789: {
                'content': {
                    'title': 'Пиздюк иваныч',
                    'header': 'В задачи вакансии входит ебать мозги'
                }
            }
        }
        vacancy_info = get_vac_by_id.get(vac_id, False)
        if vacancy_info:
            title: str = "💥 Название позиции: " + vacancy_info['content']['title'] + '\n'
            text: str = title + "💥 Описание: " + vacancy_info['content']['header'] + '\n' + \
                        cfg.app.hosts.sbervacanсy.host.format(str(vac_id))
            text: str = text + '\n' "Показать еще❓"
            await send_message(cfg.app.hosts.tlg.host, m.message.chat.id,
                               remove_html_in_dict(text)[:4095],
                               buttons=['Да', 'Нет'],
                               one_time_keyboard=False)
            return 1
        else:
            text = '🤓 К сожалению, вакансий больше нет❗️'
            await send_message(cfg.app.hosts.tlg.host,
                               m.message.chat.id,
                               text,
                               remove_keyboard=True)
            return 0

    else:
        text = '💥 Пока, возвращайся еще❗️'
        await send_message(cfg.app.hosts.tlg.host,
                           m.message.chat.id,
                           text,
                           remove_keyboard=True)
        return 0


async def goodbye_message(m: Updater):
    text = '💥 Пока, возвращайся еще❗️'
    await send_message(cfg.app.hosts.tlg.host,
                       m.message.chat.id,
                       text,
                       remove_keyboard=True)
    return 0
