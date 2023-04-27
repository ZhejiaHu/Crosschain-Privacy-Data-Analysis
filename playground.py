from database.persistance import connect_db, close_db, save_account, save_transaction
from model.account import Account
from model.transaction import Transaction
from remote.account_remote import get_account_info_from_remote, get_normal_transaction_from_account
from algorithm import account_transaction_crawler
from remote.connext_remote import get_atom_transactions_from_transfer, get_latest_transfers
from datastructure.Graph import Graph
import in_mem

"""
    27/04/2022: From cross chain (Connext), get latest transfer 
    Test 1: Chain Id 1 -- Ethereum Mainnet
    
    Test data graph structure
"""


def update_graph_transaction(txn: Transaction, graph):
    sender, receiver = txn.from_account, txn.to_account
    in_mem.in_mem_account_ids[sender] = get_account_info_from_remote(sender)
    in_mem.in_mem_account_ids[receiver] = get_account_info_from_remote(receiver)
    graph.add_edge_transaction(in_mem.in_mem_account_ids[sender], in_mem.in_mem_account_ids[receiver], in_mem.in_mem_txns_id[txn.txn_hash])


def update_graph(transfers, graph):
    for transfer in transfers:
        origin_txn, dest_txn = transfer.origin_txn, transfer.destination_txn
        in_mem.in_mem_txns_id[origin_txn.txn_hash] = origin_txn
        in_mem.in_mem_txns_id[dest_txn.txn_hash] = dest_txn
        update_graph_transaction(origin_txn, graph)
        update_graph_transaction(dest_txn, graph)


if __name__ == "__main__":
    chain_id = 1
    graph = Graph()
    origin_transfers, dest_tranfers = get_latest_transfers(chain_id)
    update_graph(origin_transfers, graph)
    update_graph(dest_tranfers, graph)
    print(graph)





