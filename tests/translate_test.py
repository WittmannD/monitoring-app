import asyncio
import json
import logging

from models import TranslateRequestModel
from translator import Translator


async def test() -> None:
    data = [
        TranslateRequestModel('미래 남편 누구게?(연재)', 'ru')
    ]

    translator = Translator()
    result = await translator.translate(data)

    logging.info(json.dumps(result, indent=4))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
