from os import environ
from PyQt5.QtCore import QSettings

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ROOT = environ.get('ROOT')
CONFIG_PATH = environ.get('CONFIG_PATH')
ASSETS_PATH = environ.get('ASSETS_PATH')
LOGGING = environ.get('LOGGING').lower() == 'true'
GOOGLE_API_KEY = environ.get('GOOGLE_API_KEY')

APP_SETTINGS = QSettings()
