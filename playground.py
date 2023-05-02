from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.account_remote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler
from remote.connext_remote import get_atom_transactions_from_transfer, get_latest_transfers, perform_scrawl_from_latest_transfer, perform_scrawl_from_latest_transfer_worker
from datastructure.Graph import Graph
from remote import construct_smart_contract_object, get_internal_transaction_from_transaction_hash, get_token_swap_from_transaction_hash
from model import get_method_id, TokenType
import eth_abi
import sha3
import in_mem

"""
    02/05/2023: Test obtaining token transaction in the transaction:
        -- Test 1:
            -- Chain name: Arbitrum
            -- Transaction hash: https://arbiscan.io/tx/0xf052c61563ca61f91982b5db08a3cc7188f59aa49a70efd0830bf588a59bce2f
            -- Expected result: Should contains 7 token behaviours. 
            -- Returned result: [1, 2, 3, 4, 5, 6, 7]
"""


if __name__ == "__main__":
    results = get_token_swap_from_transaction_hash("0xab7a7257fa475744007ce80d4f59d02397d235621894ab0279600fe339375bd2",
                                                   27855229,
                                                       "0x49b77781f3c315b34bf2d4211451d45c19038b7d",
                                                   56,
                                                   TokenType.T20)
    print("Number of results {}".format(len(results)))
    for result in results: print(result)




