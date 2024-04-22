
from web3 import Web3
from web3.eth import AsyncEth

from util.utils import sleeping
from .data import DATA
from .sleeping import sleep
from setting import CHECK_GWEI, MAX_GWEI
from loguru import logger

async def get_gas(network: str):
    try:
        w3 = Web3(
            Web3.AsyncHTTPProvider(str(DATA[network]['rpc'])),
            modules={"eth": (AsyncEth,)},
        )
        gas_price = await w3.eth.gas_price
        gwei = w3.from_wei(gas_price, 'gwei')
        return gwei
    except Exception as error:
        logger.error(error)


async def wait_gas_ethereum(network: str):
    while True:
        gas = await get_gas(network)
        if gas > MAX_GWEI:
            logger.info(f'Current GWEI: {gas} > {MAX_GWEI}')
            sleeping(60, 70)
        else:
            logger.info(f"GWEI is normal | current: {gas} < {MAX_GWEI}")
            break

def check_gas(network: str = 'ethereum'):
    def decorator(func):
        async def _wrapper(*args, **kwargs):
            if CHECK_GWEI:
                await wait_gas_ethereum(network)
            return await func(*args, **kwargs)
        return _wrapper
    return decorator