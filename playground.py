from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.account_remote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler
from remote.connext_remote import get_atom_transactions_from_transfer, get_latest_transfers, perform_scrawl_from_latest_transfer, perform_scrawl_from_latest_transfer_worker
from datastructure.Graph import Graph
from remote import construct_smart_contract_object, get_internal_transaction_from_transaction_hash, get_token_swap_from_transaction_hash, get_handler, get_transactions_from_latest_block
from model import get_method_id, TokenType
import eth_abi
import sha3
import in_mem

"""
    04/05/2023: Test transactions with events emitted
"""


if __name__ == "__main__":
    lst = get_transactions_from_latest_block(1)
    for tr in lst:
        print(tr)




