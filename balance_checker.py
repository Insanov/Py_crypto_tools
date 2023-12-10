import json
from eth_account import Account
# import secrets
from web3 import Web3


def connect_establish(rpc):
    w3 = Web3(Web3.HTTPProvider(rpc))

    return w3


def balance_check(w3object, address, wallet):
    checksum_wallet = Web3.to_checksum_address(wallet)
    checksum_address = Web3.to_checksum_address(address)
    abi = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')
    checkable_contract = w3object.eth.contract(
        address=checksum_address, abi=abi)

    return checkable_contract.functions.balanceOf(checksum_wallet).call() / 10 ** 6


def all_contracts_check(wallet):
    RPCs_dict = {"POLYGON": "https://rpc.ankr.com/polygon",
                 "AVALANCHE": "https://rpc.ankr.com/avalanche",
                 "ARBITRUM": "https://rpc.ankr.com/arbitrum",
                 "OPTIMISM": "https://rpc.ankr.com/optimism"}

    USDT_contracts_dict = {"POLYGON": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
                           "AVALANCHE": "0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7",
                           "ARBITRUM": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
                           "OPTIMISM": "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58"}

    w3s_list = list(map(connect_establish, RPCs_dict.values()))
    w3s_dict = {chain: w3object for chain,
                w3object in zip(RPCs_dict.keys(), w3s_list)}

    USDT_balances_dict = {}
    for chain, w3object, address in zip(w3s_dict.keys(), w3s_dict.values(), USDT_contracts_dict.values()):
        USDT_balances_dict[chain] = balance_check(w3object, address, wallet)

    return USDT_balances_dict
