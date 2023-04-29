from algorithm import account_transaction_crawler
from model.connext_transfer import ConnextTransfer
from model.transaction import Transaction
from requests import get, post
from threading import Thread
from typing import List
import util

CHAIN_ID_TO_SUBGRAPH_API = {
    1: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-mainnet",  # mainnet
    10: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-optimism",  # optimism
    42161: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-arbitrum-one",  # Arbitrum One
    137: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-polygon",  # polygon
    56: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-bnb",  #bnb
    100: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-gnosis" #gnosis
}


ORIGIN_TXN_GRAPH_QUERY = """
    query OriginTransfer {{
      originTransfers(
        where: {{
          transferId: "{}"
        }}
      ) {{
        # Meta Data
        chainId
        blockNumber
        nonce
        transferId
        to
        delegate
        receiveLocal
        callData
        slippage
        originSender
        originDomain
        destinationDomain
        transactionHash
        bridgedAmt
        status
        timestamp
        normalizedIn
        # Asset Data
        asset {{
          id
          adoptedAsset
          canonicalId
          canonicalDomain
        }}
      }}
    }}
"""

DEST_TXN_GRAPH_QUERY = """
    query DestinationTransfer {{
      destinationTransfers(
        where: {{
          transferId: "{}"
        }}
      ) {{
        # Meta Data
        chainId
        nonce
        transferId
        to
        callData
        originDomain
        destinationDomain
        delegate
        # Asset Data
        asset {{
          id
        }}
        bridgedAmt
        # Executed event Data
        status
        routers {{
          id
        }}
        amount
        originSender
        # Executed Transaction
        executedCaller
        executedTransactionHash
        executedTimestamp
        executedGasPrice
        executedGasLimit
        executedBlockNumber
        # Reconciled Transaction
        reconciledCaller
        reconciledTransactionHash
        reconciledTimestamp
        reconciledGasPrice
        reconciledGasLimit
        reconciledBlockNumber
        routersFee
        slippage
        executedTxOrigin
      }}
    }}
"""

GET_LATEST_TRANSFER_ORIGIN = """
    query LatestTransfers {
      originTransfers(first:10) {
        transferId
      }
      
      destinationTransfers(first:10) {
        transferId
      }
    }
"""


def _query_connext_transfer(transfer_id):
    query_address = util.CONNEXT_TRANSFER_API.format(transfer_id)
    transfer_metadata = get(query_address).json()
    return transfer_metadata[0]


def _query_atom_transaction(transfer_id, chain_id, is_origin, result: List[Transaction]):
    query_template = ORIGIN_TXN_GRAPH_QUERY if is_origin else DEST_TXN_GRAPH_QUERY
    response = post(CHAIN_ID_TO_SUBGRAPH_API[int(chain_id)], "", json={"query": query_template.format(transfer_id)}).json()["data"]
    txn_list = response["originTransfers" if is_origin else "destinationTransfers"]
    if len(txn_list) == 0: print(f"Not valid transaction query with transfer id {transfer_id} on chain id {chain_id} and whether is origin transaction {is_origin}"); return
    txn_metadata = txn_list[0]
    result[0 if is_origin else 1] = Transaction(txn_metadata["transactionHash"] if is_origin else txn_metadata["executedTransactionHash"],
                       1 if txn_metadata["status"] == "XCalled" else 0,
                       txn_metadata["timestamp"] if is_origin else txn_metadata["executedTimestamp"],
                       txn_metadata["delegate"] if is_origin else txn_metadata["executedTxOrigin"],
                       txn_metadata["originSender"] if is_origin else txn_metadata["to"],
                       txn_metadata["blockNumber"] if is_origin else txn_metadata["executedBlockNumber"],
                       txn_metadata["bridgedAmt"] if is_origin else txn_metadata["amount"],
                       -1,
                       int(txn_metadata["chainId"])
                       )
    if is_origin and result[0].from_account == result[0].to_account: result[0].to_account = util.CONNEXT_CONTRACT_ADDRESS[int(chain_id)]


def get_atom_transactions_from_transfer(transfer_id):
    metadata = _query_connext_transfer(transfer_id)
    origin_chain_id, dest_chain_id = metadata["origin_chain"], metadata["destination_chain"]
    result_txns = [None, None]
    origin_query_thread, dest_query_thread = Thread(target=_query_atom_transaction, args=(transfer_id, origin_chain_id, True, result_txns)), Thread(_query_atom_transaction(transfer_id, dest_chain_id, False, result_txns))
    origin_query_thread.start(), dest_query_thread.start()
    origin_query_thread.join(), dest_query_thread.join()
    assert result_txns[0] is not None and result_txns[1] is not None
    return ConnextTransfer(transfer_id, result_txns[0], result_txns[1])


def get_latest_transfers(chain_id):
    query_address = CHAIN_ID_TO_SUBGRAPH_API[chain_id]
    response = post(query_address, "", json={"query": GET_LATEST_TRANSFER_ORIGIN}).json()["data"]
    get_transfer_id = lambda tr: tr["transferId"]
    origin_transfer_ids, destination_transfer_ids = map(get_transfer_id, response["originTransfers"]), map(get_transfer_id, response["destinationTransfers"])
    origin_transfers, destination_transfers = map(get_atom_transactions_from_transfer, origin_transfer_ids), map(get_atom_transactions_from_transfer, destination_transfer_ids)
    return origin_transfers, destination_transfers


def perform_scrawl_from_transaction_list(txn_list: List[Transaction], chain_id):
    init_addresses = set(map(lambda txn: txn.from_account, txn_list)) | set(map(lambda txn: txn.to_account, txn_list))
    account_traversed, txn_traversed = account_transaction_crawler(init_addresses, chain_id)
    return account_traversed, txn_traversed


def perform_scrawl_from_latest_transfers_chain(main_chain):
    origin_transfers, destination_transfers = get_latest_transfers(main_chain)
    txn_as_origin, txn_as_destination = list(map(lambda tr: tr.origin_txn, origin_transfers)), list(map(lambda tr: tr.destination_txn, destination_transfers))
    txn_on_curr_chain = txn_as_origin + txn_as_destination
    return perform_scrawl_from_transaction_list(txn_on_curr_chain, main_chain)


def perform_scrawl_from_latest_transfer():
    for chain_id in util.SUPPORT_CHAIN_ID:
        print("Starting web scrawling on chain: {}".format(chain_id))
        curr_accounts, curr_txns = perform_scrawl_from_latest_transfers_chain(chain_id)
        for acc in curr_accounts: print(acc)
        for txn in curr_txns: print(txn)







