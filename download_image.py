from client import HttpClient
from urllib.parse import quote
from collections import namedtuple
from typing import List, Dict
import aiohttp
import asyncio
import logging
import json


async def download_image(url):
    filename = url.split('/')[-1]
    path = os.path.join('./images/cover/', filename)

    response = requests.get(url)

    file = open(path, 'wb')
    file.write(response.content)
    file.close()

    return path
