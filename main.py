import sys
import asyncio
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import questionary
from util.utils import WALLETS, show_dev_info
from util.sleeping import sleep
from questionary import Choice
from loguru import logger
from module_setting import *
from setting import *

def get_wallets():
    wallets = [
        {
            "id": _id,
            "key": key,
        } for _id, key in enumerate(WALLETS, start=1)
    ]
    return wallets

def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Use DeBridge", startdebridge),
            Choice("2) Use Nitro", startnitrobridge),
            Choice("3) Do random bridge", randomBridge),
            Choice("4) Exit", "exit"),
        ],
          qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("Bye bye")
        sys.exit()
    return result

async def run_module(module, account_id, key):
    try:
        await module(account_id, key)
    except Exception as e:
        logger.error(e)
    await sleep(SLEEP_FROM, SLEEP_TO)

def _async_run_module(module, account_id, key):
    asyncio.run(run_module(module, account_id, key))

def main(module):
    wallets = get_wallets()
    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                _async_run_module,
                module,
                account.get("id"),
                account.get("key")
            )
            time.sleep(random.randint(SLEEP_FROM, SLEEP_TO))

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    show_dev_info()
    module = get_module()    
    main(module)

