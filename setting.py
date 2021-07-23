from os import environ, path
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

ROOT = path.dirname(path.abspath(__file__))
CONFIG_PATH = path.join(ROOT, (environ.get('CONFIG_PATH')))
LOGGING = environ.get('LOGGING').lower() == 'true'
