from .setup import get_handler
from .transaction_remote import get_transaction_from_transaction_hash_multi_process
from datastructure import Graph, construct_graph_from_transactions
import multiprocessing

handler = get_handler()


def construct_graph_in_block_num(block_num):
    txn_hashes = list(map(lambda txn: txn.hex(), handler.get_block(block_num).transactions))[:20]
    num_txn = len(txn_hashes)
    print("{} number of hashes is included in the establish of graph.".format(num_txn))
    managers = multiprocessing.Manager().list(range(num_txn))
    for group in range(num_txn // 5):
        workers = []
        for i in range(group * 5, (group + 1) * 5):
            curp = multiprocessing.Process(target=get_transaction_from_transaction_hash_multi_process, args=(txn_hashes[i], managers, i))
            workers.append(curp)
            curp.start()
        for i in range(5): workers[i].join()
    managers = list(filter(lambda manager: manager is not None, managers))
    print("The number of valid transactions are {}.".format(len(managers)))
    return construct_graph_from_transactions(managers)


def construct_graph_from_latest_block():
    latest_block_number = handler.get_block_number()
    print("The current block is {}".format(latest_block_number))
    return construct_graph_in_block_num(latest_block_number)
