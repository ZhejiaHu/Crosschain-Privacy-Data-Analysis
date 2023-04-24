from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.accountRemote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler

"""
24/04/2023: Crawl a transaction from etherscan and persist in the database
Example transaction: https://etherscan.io/tx/0x69fdc8e3714dd58a1608e9e74b9d5ad6808ad2f7658e75d55c1d658c0cd11d87
Example user: https://etherscan.io/address/0x2ab8c66af333f80ce2bae82fc83a9a970e7740fa
"""


if __name__ == "__main__":
    account_addr = "0x2ab8c66af333f80ce2bae82fc83a9a970e7740fa"
    account_visited, transaction_visited = account_transaction_crawler(account_addr)
    print("Accounts visited:")
    for account in account_visited: print(account)
    print("\nTransactions visited:")
    for txn in transaction_visited: print(txn)

