import random
import aiohttp
from loguru import logger
from random import uniform
from aiohttp import ClientSession, TCPConnector
from util.utils import WALLET_PROXIES
from setting import USE_PROXY
import time

def get_user_agent():
    random_version = f"{uniform(520, 540):.2f}"
    return (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random_version} (KHTML, like Gecko)'
            f' Chrome/123.0.0.0 Safari/{random_version} Edg/123.0.0.0')

async def make_request(key: str, method:str = 'GET', url:str = None, params: dict = None,
                           data:str = None, json:dict = None):

        headers = {'User-Agent': get_user_agent(), "Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            if USE_PROXY == True:
                proxy = WALLET_PROXIES[key]
            else:
                proxy = None
            async with session.request(method=method, url=url, headers=headers, data=data, json=json,
                                                params=params,  proxy=proxy) as response:

                data = await response.json()
                if response.status in [200, 301]:
                    return data
                else:
                    logger.info(f'API error: {data}')
