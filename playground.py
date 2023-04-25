from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.accountRemote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler


if __name__ == "__main__":
    connect_db()
    account_addr = "0x56Ae7d260b334FBCad48D11dc6a6056d1cD2fbc4"
    account_visited, transaction_visited = account_transaction_crawler(account_addr)
    print("Accounts visited:")
    for account in account_visited: print(account); save_account(account)
    print("\nTransactions visited:")
    for txn in transaction_visited: print(txn); save_transaction(txn)
    close_db()

