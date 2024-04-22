import math
import random
import time
import tqdm
import asyncio
from art import tprint
from loguru import logger
from setting import RETRY
from .sleeping import sleep

with open(f"core/abi/erc_20.json", "r") as f:
    ERC20_ABI = [row.strip() for row in f]

with open(f"user_data/wallets.txt", "r") as f:
    WALLETS = [row.strip() for row in f]

with open(f"user_data/proxies.txt", "r") as f:
    PROXIES = [row.strip() for row in f]

def get_wallet_proxies(wallets, proxies):
    try:
        result = {}
        for i in range(len(wallets)):
            result[wallets[i]] = proxies[i % len(proxies)]
        return result
    except: None
    
def intToDecimal(qty, decimal):
    return int(qty * 10**decimal)

def decimalToInt(qty, decimal):
    return float(qty / 10**decimal)

def round_to(num, digits=3):
    try:
        if num == 0: return 0
        scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
        if scale < digits: scale = digits
        return round(num, scale)
    except: return num

def sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)

async def async_sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        await asyncio.sleep(1)
        
def show_dev_info():
    tprint("Dropsoft_debridge")
    print("")
    print("\033[36m" + "VERSION: " + "\033[34m" + "1.0" + "\033[34m")
    print("\033[36m" + "DEV: " + "\033[34m" + "https://t.me/drop_software" + "\033[34m")
    print("\033[36m" +"GitHub: " + "\033[34m" + "https://github.com/Dropsoft-soft/De-bridge" + "\033[34m")
    print("\033[36m" + "DONATION EVM ADDRESS: " + "\033[34m" + "0xb1b1ac053248a2C88e32140e4691d2A8Be6Ab9c9" + "\033[0m")
    print()

WALLET_PROXIES  = get_wallet_proxies(WALLETS, PROXIES)

def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries < RETRY+1:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                info = (str(e)[:100] + '..') if len(str(e)) > 100 else str(e)
                await sleep(10, 60)
                retries += 1

    return wrapper
