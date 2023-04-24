from model import Account, Transaction
from remote import get_account_info_from_remote, get_normal_transaction_from_account
import threading


def account_transaction_crawler(init_address, max_depth=50, max_width=50):
    account_visited, transaction_visited, threads = set(), set(), []

    def depth_first_search(curr_address, curr_depth):
        account_visited.add(curr_address)
        recent_txns = get_normal_transaction_from_account(curr_address)[:max_width]
        for next_txn in recent_txns:
            receiver_address = next_txn.to_account
            transaction_visited.add(next_txn)
            if receiver_address in account_visited or curr_depth + 1 > max_depth: continue
            curr_thread = threading.Thread(target=depth_first_search, args=(receiver_address, curr_depth + 1))
            curr_thread.start()
            threads.append(curr_thread)

    main_thread = threading.Thread(target=depth_first_search, args=(init_address, 0))
    main_thread.start()
    threads.append(main_thread)
    for thread in threads: thread.join()
    return map(lambda acc: get_account_info_from_remote(acc), account_visited), transaction_visited







