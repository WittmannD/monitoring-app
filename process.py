import asyncio
import os
from datetime import datetime
from typing import Iterable

import aiofiles

from client import HttpClient
from models import TranslateRequestModel, PreparedTitleModel
from setting import ASSETS_PATH
from translator import Translator


class DataProcessing:
    storage = set()

    def __init__(self, controller, http_client=HttpClient()):
        self.controller = controller

        self.http_client = http_client
        self.translator = Translator(http_client=http_client)

    @staticmethod
    def find_by_isbn(data: Iterable, isbn_set: Iterable) -> list:
        return list(filter(lambda o: o['EA_ISBN'] in isbn_set, data))

    @staticmethod
    def prepare_isbn(data: Iterable) -> set:
        return set(item['EA_ISBN'] for item in data)

    async def download_image(self, url):
        if not url:
            return os.path.join(ASSETS_PATH, 'covers', 'cover.jpg')

        filename = url.split('/')[-1]
        path = os.path.join(ASSETS_PATH, 'covers', filename)

        async def request_callback(response):
            if response.status == 200:
                f = await aiofiles.open(path, mode='wb')
                await f.write(await response.read())
                await f.close()

        try:
            await self.http_client.request(
                url=url,
                timeout=30,
                method='GET',
                cb=request_callback
            )
        except Exception:
            return os.path.join(ASSETS_PATH, 'covers', 'cover.jpg')

        return path

    async def translate(self, data):
        translated = await self.translator.translate([
            TranslateRequestModel(data['TITLE'], 'en'),
            TranslateRequestModel(data['TITLE'], 'ru')
        ])
        return dict(
            title_kor=translated[0].sourceText,
            title_eng=translated[0].translatedText,
            title_rus=translated[1].translatedText
        )

    async def handler(self, data):
        translate_task = asyncio.create_task(self.translate(data))
        download_image_task = asyncio.create_task(self.download_image(data['TITLE_URL']))

        translated_data, image_path = await asyncio.gather(translate_task, download_image_task)

        title = PreparedTitleModel(
            **translated_data,
            cover=image_path,
            isbn=data['EA_ISBN'],
            datetime=datetime.now().strftime('%x %X'),
            description='',
            keyword=''
        )
        self.controller.tilted_listener.emit(title)

    def run(self, data: dict) -> None:
        data: list = data['response']['docs']

        new_isbn = self.prepare_isbn(data)
        existing_isbn = new_isbn.difference(self.storage)

        if existing_isbn:
            self.storage = new_isbn
            new_data = self.find_by_isbn(data, existing_isbn)

            asyncio.gather(*[self.handler(item) for item in new_data])
