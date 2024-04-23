import asyncio
from core import *
import random
from loguru import logger

async def startdebridge(_id, key):
    '''
    Bridge native coins via https://app.debridge.finance/deswap
    Chains : ethereum | bsc | optimism | arbitrum | base | avalanche | polygon | linea 
    Support native coins
    '''
    from_chain              = 'base' # From network
    to_chain                = 'arbitrum' # To network
    
    amount_from             = 0.0005 # Amount from to bridge tokens
    amount_to               = 0.0009 # Amount to to bridge tokens
    bridge_all_balance      = False # True / False. IF True, swap all balance
    debridge = DeBridge(_id, key, from_chain)
    await debridge.bridge(
        from_chain, to_chain, amount_from, amount_to, bridge_all_balance
    )

async def startnitrobridge(_id, key):
    '''
    Bridge coins via https://nitro.routerprotocol.com/ or swap
    Chains : ethereum | optimism | bsc | arbitrum | polygon | zksync | linea | base | scroll | blast
    '''
    from_chain              = 'base' # From network
    to_chain                = 'arbitrum' # To network
    
    amount_from             = 0.001 # Amount from to bridge tokens
    amount_to               = 0.001 # Amount to to bridge tokens
    bridge_all_balance      = False # True / False. IF True, swap all balance
    nitrobridge = NitroBridge(_id, key, from_chain)
    await nitrobridge.bridge(
        from_chain, to_chain,amount_from, amount_to, bridge_all_balance
    )

async def randomBridge(_id, key):
    # Random chain and random platform will pick to do bridge
    all_chains  = ['ethereum', 'optimism',  'bsc', 'arbitrum', 'base', 'avalanche', 'polygon', 'linea']
   
    # User settings
    amount_from             = 0.0001    # Amount from to bridge tokens
    amount_to               = 0.0001    # Amount to to bridge tokens
    bridge_all_balance      = False     # True / False. IF True, swap all balance
    
    # DO NOT TOUCH!!!
    platforms   = ['debridge', 'nitro']
    from_chain  = random.choice(list(all_chains))
    to_chain    = random.choice(list(all_chains))
    selected_platform       = random.choice(list(platforms))
    if selected_platform == 'debridge':
        debridge = DeBridge(_id, key, from_chain)
    else:
        debridge = NitroBridge(_id, key, from_chain)
    logger.info(f'Random platform: {selected_platform}')
    await debridge.bridge(
        from_chain, to_chain,amount_from, amount_to, bridge_all_balance
    )


async def circularBridge(_id, key):
    # bridge from 1 chain to second untill list is ended
    chains  = ['ethereum', 'optimism',  'bsc', 'arbitrum', 'base', 'avalanche', 'polygon', 'linea']
   
    # User settings
    amount_from             = 0.0001    # Amount from to bridge tokens
    amount_to               = 0.0001    # Amount to to bridge tokens
    bridge_all_balance      = False     # True / False. IF True, swap all balance
    len_array = len(chains)
    for index, chain in enumerate(chains):    
        debridge = DeBridge(_id, key, chain)
        if len_array == index+1:
            logger.info(f'Finished')
            return
        to_chain = chains[index+1]
        result = await debridge.bridge(
            chain, to_chain, amount_from, amount_to, bridge_all_balance
        )
        await asyncio.sleep(1)
        print(result)

