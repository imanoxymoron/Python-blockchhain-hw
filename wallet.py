from constants import *
from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware

import subprocess
import json
import os
from dotenv import load_dotenv


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
s3.eth.setGasPriceStrategy(medium_gas_price_strategy)

load_dotenv('homework.env')

private_key = os.getenv('mnemonic')

print(type(private_key))
./derive -g --mnemonic="oil traffic blind stumble quote weekend wise tank clay layer slot cash" --cols=path,address,privkey,pubkey --coin="BTC" --numderive=3 --format=json

def derive_wallet(coin=BTC, mnemonic=private_key, depth=3):
    command = f'./derive -g --mnemonic={mnemonic} --cols=path,address,privkey,pubkey --coin={coin} --numderive={depth} --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

derive_wallet()

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    
def create_tx(coin, account, to, amount):
    if coin == ETH:
        value = w3.toWei(amount, "ether")
        gasEstimate = w3.eth.estimateGas({"to":to, "from":account,"amount":value})
        return {
            "to": to,
            "from": account,
            "value": value,
            "gas": gasEstimate,
            "gasPrice": w3.eth.generateGasPrice(),
            "nonce": w3.eth.getTransactionCount(account),
            "chainId": w3.eth.chain_df
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to,amount,BTC)])
    
def send_tx(coin, account, to, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account.address, to, amount)
        signed = account.signTransaction(raw_tx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    if coin == BTCTEST:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)

coin = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST)
}

print(coins)
