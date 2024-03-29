from model import Account, Transaction
from remote import get_account_info_from_remote, get_normal_transaction_from_account
import threading


def account_transaction_crawler(init_addresses, chain_id, max_depth=10, max_width=10):
    account_visited, transaction_visited, threads = set(), set(), []

    def depth_first_search(curr_address, curr_depth):
        account_visited.add(curr_address)
        recent_txns = get_normal_transaction_from_account(curr_address, chain_id)[:max_width]
        for next_txn in recent_txns:
            if next_txn in transaction_visited: continue
            receiver_address = next_txn.receiver
            transaction_visited.add(next_txn)
            if receiver_address in account_visited or curr_depth + 1 > max_depth: continue
            curr_thread = threading.Thread(target=depth_first_search, args=(receiver_address, curr_depth + 1))
            curr_thread.start()
            threads.append(curr_thread)

    for init_address in init_addresses:
        main_thread = threading.Thread(target=depth_first_search, args=(init_address, 0))
        main_thread.start()
        threads.append(main_thread)
        for thread in threads: thread.join()
    return map(lambda acc: get_account_info_from_remote(acc, chain_id), account_visited), transaction_visited


def construct_graph_from_latest_block(block_id, chain_id):
    pass






