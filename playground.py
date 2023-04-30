from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.account_remote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler
from remote.connext_remote import get_atom_transactions_from_transfer, get_latest_transfers, perform_scrawl_from_latest_transfer, perform_scrawl_from_latest_transfers_chain
from datastructure.Graph import Graph
from remote import construct_smart_contract_object, get_internal_transaction_from_transaction_hash
import in_mem

"""
    30/04/2023: Obtain the latest transfers from connext, and for each transfer, perform a web scrawl, with internal transactions
"""


if __name__ == "__main__":
    perform_scrawl_from_latest_transfer()
    #print(get_internal_transaction_from_transaction_hash("0xd8daee51dff27874a334499f1ebb2d2f33359bba0a8c8c752a6399547aa5579e", 56))





