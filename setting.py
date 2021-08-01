from os import environ, path
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

ROOT = environ.get('ROOT')
CONFIG_PATH = environ.get('CONFIG_PATH')
ASSETS_PATH = environ.get('ASSETS_PATH')
LOGGING = environ.get('LOGGING').lower() == 'true'
GOOGLE_API_KEY = environ.get('GOOGLE_API_KEY')
