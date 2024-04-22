from util.data import DATA
from util.gas_checker import check_gas
from util.http_client import make_request
from util.utils import intToDecimal, retry
from .client import WebClient
from loguru import logger
from web3 import Web3
import random

class DeBridge(WebClient):
    def __init__(self, id:int, key: str, chain: str) -> None:
        super().__init__(id=id, key=key, chain=chain)
        logger.info(f'account id: {self.id} address: {self.address}')
    
    @retry
    @check_gas()
    async def bridge(self, from_chain, to_chain, amount_from, amount_to, full_balance=False):
        module_string = f'{self.id} | DeBridge from {from_chain} => {to_chain}'
        logger.info(module_string)
        ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
        from_token  = ZERO_ADDRESS
        to_token    = ZERO_ADDRESS
        from_token = Web3.to_checksum_address(from_token)
        to_token   = Web3.to_checksum_address(to_token)
        keep_value = 0.0011
        if full_balance == True: 
            amount_ = self.get_balance(self.key, self.chain, '') - keep_value
        else: amount_ = round(random.uniform(amount_from, amount_to), 8)
        amount = intToDecimal(amount_, 18)
        router_data = await self.getQuote(self.chain_id, DATA[to_chain]["chain_id"], from_token, to_token, amount)
        if router_data == None:
            logger.error('route not available. Visit site to verify possible routes')
            return
        response_data = await self.buildTx(router_data)
        tx_data = response_data["tx"]
        if tx_data == None:
            logger.error('route not available. Visit site to verify possible routes')
            return
        
        tx = {
            "chainId": await self.web3.eth.chain_id,
            "from": self.address,
            "value": amount,
            "nonce": await self.web3.eth.get_transaction_count(self.address),
            'gas': 0,
            "to": Web3.to_checksum_address(tx_data["to"]),
            'gasPrice': int(await self.web3.eth.gas_price*1.05),
            "data": tx_data["data"],
            "value": int(tx_data["value"]),
        }

        gasLimit = int(await self.web3.eth.estimate_gas(tx)*1.1)
        tx.update({'gas': gasLimit})
        status, tx_link  = await self.send_tx(tx)
        if status == 1:
            logger.success(f'{module_string} | {tx_link}')
        else:
            logger.error(f'{module_string} | tx is failed | {tx_link}')
    
    async def getQuote(self, from_chain_id, to_chain_id, from_token, to_token, amount):
        url = "https://api.dln.trade/v1.0/dln/order/quote"
        params = {
            "srcChainId": from_chain_id,
            "srcChainTokenIn": from_token,
            "srcChainTokenInAmount": amount,
            "dstChainId": to_chain_id,
            "dstChainTokenOut": to_token,
            "prependOperatingExpenses": 1
        }
        return await make_request(key=self.key, url=url, params=params)

    async def buildTx(self, json):
        url = "https://api.dln.trade/v1.0/dln/order/create-tx"
        params = {
            "srcChainId": int(json['estimation']['srcChainTokenIn']['chainId']),
            "srcChainTokenIn": json['estimation']['srcChainTokenIn']['address'],
            "srcChainTokenInAmount": json['estimation']['srcChainTokenIn']['amount'],
            "dstChainId": int(json['estimation']['dstChainTokenOut']['chainId']),
            "dstChainTokenOut": json['estimation']['dstChainTokenOut']['address'],
            "dstChainTokenOutAmount": json['estimation']['dstChainTokenOut']['amount'],
            "dstChainTokenOutRecipient": self.address,
            "srcChainOrderAuthorityAddress": self.address,
            "dstChainOrderAuthorityAddress": self.address,
            'affiliateFeePercent':0.1,
            'affiliateFeeRecipient':'0x387c6e7fe88042966acf9eac1852e0f101e4b37d'
        }
        return await make_request(key=self.key,  url=url, params=params)



