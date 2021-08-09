from plyer import notification
from plyer.utils import platform

from setting import APP_ID


class Notifier:
    app = APP_ID

    def show(self):
        notification.notify(
            title='Found new records',
            message='hh',
            app_name='Monitoring Bot',
            ticker='Seoji Bot new title'
        )

if __name__ == '__main__':
    noti = Notifier()
    noti.show()
