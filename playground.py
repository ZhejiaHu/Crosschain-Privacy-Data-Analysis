from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.account_remote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler
from remote.connext_remote import get_atom_transactions_from_transfer, get_latest_transfers, perform_scrawl_from_latest_transfer, perform_scrawl_from_latest_transfers_chain
from datastructure.Graph import Graph
from remote import construct_smart_contract_object
import in_mem

"""
    29/04/2023: Obtain the latest transfers from connext, and for each transfer, perform a web scrawl.
"""


if __name__ == "__main__":
    perform_scrawl_from_latest_transfer()





