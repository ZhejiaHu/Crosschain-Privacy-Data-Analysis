from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.account_remote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler
from remote.connext_remote import get_atom_transactions_from_transfer

"""
    26/04/2022: From cross chain (Connext) transaction to obtain pair of atomic transactions.
    Test 1: https://connextscan.io/tx/0x79cec0063ba8a06fc29a2eb948165e33705b81ef6b40d8a0d61bd0c2f65437c1
    Test 2: https://connextscan.io/tx/0x0d925f7361946acca95f9b2473a32e082b5959c42bc51f3fb6aeaeda56d4eed0 (Problematic)
    Test 3: https://connextscan.io/tx/0xb2dc6713128b0cf95aedb1fc198b804519db70d373f26993d54784fa8846b249
    Test 4: https://connextscan.io/tx/0x179b0bc2a0ca8975f1760361412840bb636fe5cab415a6b73e75300c74b6b6a6 
    Test 5: https://connextscan.io/tx/0x4c1c2bae8c3972625157fd5f6f93aa40d8fe3c80c010fecd95eaa1dfb756f1d2
    Test 6: https://connextscan.io/tx/0x7c7d50287147875aba5b38a8ff1d90f84492d207e94c84a72e392d8019932eca
"""


if __name__ == "__main__":
    transfer_id = "0x7c7d50287147875aba5b38a8ff1d90f84492d207e94c84a72e392d8019932eca"
    connext_transfer = get_atom_transactions_from_transfer(transfer_id)
    print(connext_transfer)

