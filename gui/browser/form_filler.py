import asyncio
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QEventLoop, QTimer, Qt


from gui.browser.browser import WebView
from models import PreparedTitleModel


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


        await self.view.page.clickTo('#id_categories_chosen')
        await self.view.page.clickTo('#id_categories_chosen > div > ul > li:nth-child(1)')

        await self.view.page.clickTo('#id_categories_chosen')
        await self.view.page.clickTo('#id_categories_chosen > div > ul > li:nth-child(2)')

        await self.view.page.clickTo('#id_genres_chosen')
        await self.view.page.clickTo('#id_genres_chosen > div > ul > li:nth-child(21)')

        #await self.view.page.clickTo('#id_publishers_chosen')

        await self.view.page.evaluateJavaScript(f'''
            document.forms[0].type['value'] = 1;
            document.forms[0].status['value'] = 4;
            document.forms[0].age_limit['value'] = 0;
            document.forms[0].issue_year['value'] = 2021;
            document.forms[0].en_name['value'] = "{data.title_eng}";
            document.forms[0].rus_name['value'] = "{data.title_rus}";
            document.forms[0].another_name['value'] = "{data.title_kor}";
            document.forms[0].original_link['value'] = "{data.isbn}";
        ''')

        await self.view.page.clickTo('#id_cover')

        await self.view.page.evaluateJavaScript(f'''
            document.querySelector('button[type=submit]').scrollIntoView();
        ''')
        await self.view.page.evaluateJavaScript(f'''
            document.querySelector('button[type=submit]').scrollIntoView();
        ''')
        await self.view.page.evaluateJavaScript(f'''
            document.querySelector('button[type=submit]').scrollIntoView();
        ''')


