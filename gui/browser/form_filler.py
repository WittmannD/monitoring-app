from PyQt5.QtCore import Qt

from gui.browser.browser import WebView
from models import PreparedTitleModel
import time


def inline_cb():
    def call(func):

        def wrapper(*args, **kwargs):
            coro = func(*args, **kwargs)

            def send(val):
                try:
                    future = coro.send(val)

                except StopIteration:
                    return

                future.add_done_callback(send)

            send(None)

        return wrapper

    return call


class FormFiller:

    def __init__(self, view: WebView):
        super().__init__()
        self.view = view

    @inline_cb()
    async def start(self, data: PreparedTitleModel):
        self.view.page.file = data.cover

        filled = await self.view.page.evaluateJavaScript('window.filled')

        if not filled:

            await self.view.page.clickTo('#id_categories_chosen')
            await self.view.page.clickTo('#id_categories_chosen > div > ul > li:nth-child(1)')

            time.sleep(0.1)

            await self.view.page.clickTo('#id_categories_chosen')
            await self.view.page.clickTo('#id_categories_chosen > div > ul > li:nth-child(2)')

            time.sleep(0.1)

            await self.view.page.clickTo('#id_genres_chosen')
            await self.view.page.clickTo('#id_genres_chosen > div > ul > li:nth-child(21)')

        time.sleep(0.1)

        await self.view.page.evaluateJavaScript(f'''
            document.forms[0].type['value'] = 1;
            document.forms[0].status['value'] = 4;
            document.forms[0].age_limit['value'] = 0;
            document.forms[0].issue_year['value'] = 2021;
            document.forms[0].en_name['value'] = "{data.title_eng}";
            document.forms[0].rus_name['value'] = "{data.title_rus}";
            document.forms[0].another_name['value'] = "{data.title_kor}";
            document.forms[0].original_link['value'] = "http://seoji.nl.go.kr/landingPage?isbn={data.isbn}";
        ''')

        time.sleep(0.1)

        if not filled:
            await self.view.page.clickTo('#id_publishers_chosen')
            time.sleep(0.1)

            await self.view.page.typeText('PULSAR TEAM')
            await self.view.page.sendKeyEvent(Qt.Key_Enter, '')

        time.sleep(0.1)

        await self.view.page.evaluateJavaScript(f'''
            document.querySelector('button[type=submit]').scrollIntoView();
        ''')

        await self.view.page.evaluateJavaScript('''             
            document.querySelector('#id_publishers > option[value="5992"]').selected = true;
            document.querySelector('#id_genres > option[value="23"]').selected = true;
            document.querySelector('#id_categories > option[value="6"]').selected = true;
            document.querySelector('#id_categories > option[value="5"]').selected = true;
            
            window.filled = true;
        ''')

        await self.view.page.clickTo('#id_cover')
