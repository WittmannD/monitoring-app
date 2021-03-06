import asyncio
import json
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, QWebEngineProfile, QWebEngineSettings
from asyncqt import QEventLoop

URL = 'https://remanga.org/panel/add-titles/'


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


class ApiWrapper:

    def __init__(self, apifunc):
        self._func = apifunc

    def __call__(self, *args):
        future = asyncio.Future(loop=QEventLoop())
        self._func(*args, future.set_result)
        return future


class WebView(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(*args, **kwargs)

        self.loaded = False

        self.profile = QWebEngineProfile('storage', self)
        self.cookieStore = self.profile.cookieStore()
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        self.loadFinished.connect(self._loadFinished)

        with open('./gui/browser/cookie.json', encoding='utf-8') as f:
            self.setCookieFromJson(f)

        self.page = WebPage(self.profile, self)
        self.initUi()

    def _loadFinished(self, ok):
        self.loaded = True

    def setCookieFromJson(self, jsondata):
        data = json.load(jsondata)
        for item in data:
            cooka = QNetworkCookie()
            cooka.setDomain(item['domain'])
            cooka.setExpirationDate(datetime.fromtimestamp(item['expires']))
            cooka.setHttpOnly(item['httpOnly'])
            cooka.setSecure(item['secure'])
            cooka.setValue(item['value'].encode('utf-8'))
            cooka.setName(item['name'].encode('utf-8'))
            cooka.setPath(item['path'])
            self.cookieStore.setCookie(cooka, QtCore.QUrl(URL.replace(QtCore.QUrl(URL).path(), '')))

    def initUi(self):
        self.setPage(self.page)
        self.page.load(QtCore.QUrl(URL))

        # self.show()


class WebPage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebPage, self).__init__(*args, **kwargs)

        self.file = ''

        self.evaluateJavaScript = ApiWrapper(self._evaluateJavaScript)
        self.sendMouseEvent = ApiWrapper(self._sendMouseEvent)
        self.sendKeyEvent = ApiWrapper(self._sendKeyEvent)
        self.typeText = ApiWrapper(self._typeText)
        self.scrollTo = ApiWrapper(self._scrollTo)
        self.clickTo = ApiWrapper(self._clickTo)
        self.click = ApiWrapper(self._click)

    def chooseFiles(self, mode, oldFiles, acceptedMimeTypes):
        return [self.file]

    def _evaluateJavaScript(self, *args, **kwargs):
        super(WebPage, self).runJavaScript(*args, **kwargs)

    @inline_cb()
    async def _sendKeyEvent(self, key, text, callback):
        try:
            event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier, text=text)
            render_widget = self.view().findChild(QtWidgets.QWidget)
            QtCore.QCoreApplication.postEvent(render_widget, event)

            event = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease, key, QtCore.Qt.NoModifier, '')
            QtCore.QCoreApplication.postEvent(render_widget, event)

        except Exception as err:
            callback(False)
            raise err

        finally:
            callback(True)

    @inline_cb()
    async def _typeText(self, text, callback):
        try:
            for letter in text:
                await self.sendKeyEvent(0, letter)

        except Exception as err:
            callback(False)
            raise err

        finally:
            callback(True)

    @inline_cb()
    async def _sendMouseEvent(self, event, point, callback):
        try:
            event = QtGui.QMouseEvent(event, point, QtCore.Qt.LeftButton, QtCore.Qt.LeftButton,
                                      QtCore.Qt.NoModifier)
            render_widget = self.view().findChild(QtWidgets.QWidget)
            QtCore.QCoreApplication.postEvent(render_widget, event)

        except Exception as err:
            callback(False)
            raise err

        finally:
            callback(True)

    @inline_cb()
    async def _scrollTo(self, point, callback):
        try:
            await self.evaluateJavaScript('window.scrollTo({}, {})'.format(point.x(), point.y()))
            position = await self.evaluateJavaScript('[window.scrollX, window.scrollY]')

        except Exception as err:
            callback(False)
            raise err

        finally:
            callback(position)

    @inline_cb()
    async def _click(self, point, callback):
        try:
            await self.sendMouseEvent(QtCore.QEvent.MouseMove, point)
            await self.sendMouseEvent(QtCore.QEvent.MouseButtonPress, point)
            await self.sendMouseEvent(QtCore.QEvent.MouseButtonRelease, point)

        except Exception as err:
            callback(False)
            raise err

        finally:
            callback(True)

    @inline_cb()
    async def _clickTo(self, selector, callback):
        try:
            position = await self.evaluateJavaScript('''
                var element = document.querySelector("{0}");
                element.scrollIntoViewIfNeeded();
                var rect = element.getBoundingClientRect();
                [~~(rect.left + rect.width / 2), ~~(rect.top + rect.height / 2)];
            '''.format(selector))

            await self.click(QtCore.QPoint(*position))

        except Exception as err:
            callback(False)
            raise err

        finally:
            callback(True)
