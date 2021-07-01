import logging

from aiohttp.web_response import Response
from aiohttp_apispec import docs

from .base import BaseView
from message_schema import Updater
from plugins.statemachine import Stages
from plugins.callback import hello_message, analyze_text_and_give_vacancy, goodbye_message
from plugins.cache import AioMemCache

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

mc = AioMemCache()

state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

stage = Stages(state, mc)


class GetMessageFromTlg(BaseView):
    URL_PATH = r'/tlg/'

    @docs(summary="Endpoint для получения обновлений  с серверов телеграмма", tags=["Basic methods"],
          description="Endpoint для получения обновлений  с серверов телеграмма",
          )
    # @response_schema(PredictImageResp(), description="Возвращаем ранее добавлены комментарии к фотографии, "
    #                                                  "сортированные по дате")
    async def post(self):

        data: dict = await self.request.json()

        log.info("Message: %s", data)

        message = Updater(**data)

        await stage.next(message)

        return Response(status=200, text="ok")
