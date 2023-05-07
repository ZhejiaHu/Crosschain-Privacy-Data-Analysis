import asyncio

from .setup import get_handler
from .transaction_remote import get_transaction_from_transaction_hash_multiprocess_async_, get_transaction_from_transaction_hash, get_transaction_from_transaction_hash_multiprocess_async
from datastructure import Graph, construct_graph_from_transactions
import multiprocessing

handler = get_handler()


async def construct_graph_in_block_num(block_num):
    txn_hashes = list(map(lambda txn: txn.hex(), (await handler.get_block(block_num)).transactions))
    for hsh in txn_hashes: print(hsh)
    num_txn = len(txn_hashes)
    print("{} number of hashes is included in the establish of graph.".format(num_txn))
    managers = multiprocessing.Manager().list(range(num_txn))
    # managers = []
    # for i in range(num_txn): managers.append(await get_transaction_from_transaction_hash(txn_hashes[i]))
    for group in range(num_txn // 5):
        """
        workers = []
        for i in range(group * 5, (group + 1) * 5):
            curp = multiprocessing.Process(target=get_transaction_from_transaction_hash_multi_process, args=(txn_hashes[i], managers, i))
            workers.append(curp)
            curp.start()
        for i in range(5): workers[i].join()
        """
        workers = []
        for idx in range(group * 5, (group + 1) * 5):
            process = multiprocessing.Process(target=get_transaction_from_transaction_hash_multiprocess_async, args=(txn_hashes[idx], managers, idx))
            process.start()
            workers.append(process)
        for worker in workers: worker.join()
    workers = []
    for idx in range(num_txn // 5 * 5, num_txn):
        process = multiprocessing.Process(target=get_transaction_from_transaction_hash_multiprocess_async,
                                          args=(txn_hashes[idx], managers, idx))
        process.start()
        workers.append(process)
    for worker in workers: worker.join()
    print("The number of valid transactions are {}.".format(len(managers)))
    return construct_graph_from_transactions(managers)


async def construct_graph_from_latest_block():
    latest_block_number = await handler.get_block_number()
    print("The current block is {}".format(latest_block_number))
    return await construct_graph_in_block_num(latest_block_number)
