from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.account_remote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler
from remote.connext_remote import get_atom_transactions_from_transfer, get_latest_transfers
from datastructure.Graph import Graph
from remote import construct_smart_contract_object
import in_mem

"""
    28/04/2022: Build model for smart contract 
    Task 1: Test being able to download, parse, and construct smart contract object from Etherscan
        - Smart Contract Address 1: https://etherscan.io/address/0xd3a0b315023243632a15fd623d6f33314193df4e
        - Smart Contract Address 2: https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7
        - Smart Contract Address 3: https://etherscan.io/address/0x9d90669665607f08005cae4a7098143f554c59ef
        - Smart Contract Address 4: https://etherscan.io/address/0x805be90c8f3fa0d462450f03e8d2462160eb2287
"""


if __name__ == "__main__":
    contract_address = "0x805be90c8f3fa0d462450f03e8d2462160eb2287"
    contract = construct_smart_contract_object(contract_address)
    print(contract)





