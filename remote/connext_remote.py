from model.connext_transfer import ConnextTransfer
from model.transaction import Transaction
from requests import get, post
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


def _query_connext_transfer(transfer_id):
    query_address = util.CONNEXT_TRANSFER_API.format(transfer_id)
    transfer_metadata = get(query_address).json()
    return transfer_metadata[0]


def _query_atom_transaction(transfer_id, chain_id, is_origin):
    query_template = ORIGIN_TXN_GRAPH_QUERY if is_origin else DEST_TXN_GRAPH_QUERY
    response = post(CHAIN_ID_TO_SUBGRAPH_API[int(chain_id)], "", json={"query": query_template.format(transfer_id)}).json()["data"]
    txn_list = response["originTransfers" if is_origin else "destinationTransfers"]
    if len(txn_list) == 0: print(f"Not valid transaction query with transfer id {transfer_id} on chain id {chain_id} and whether is origin transaction {is_origin}"); return
    txn_metadata = txn_list[0]
    return Transaction(txn_metadata["transactionHash"] if is_origin else txn_metadata["executedTransactionHash"],
                       1 if txn_metadata["status"] == "XCalled" else 0,
                       txn_metadata["timestamp"] if is_origin else txn_metadata["executedTimestamp"],
                       txn_metadata["delegate"] if is_origin else txn_metadata["executedTxOrigin"],
                       txn_metadata["originSender"] if is_origin else txn_metadata["to"],
                       txn_metadata["chainId"],
                       txn_metadata["blockNumber"] if is_origin else txn_metadata["executedBlockNumber"],
                       txn_metadata["asset"]["id"],
                       -1,  # dummy
                       )


def get_atom_transactions_from_transfer(transfer_id):
    metadata = _query_connext_transfer(transfer_id)
    origin_chain_id, dest_chain_id = metadata["origin_chain"], metadata["destination_chain"]
    origin_txn, dest_txn = _query_atom_transaction(transfer_id, origin_chain_id, True), _query_atom_transaction(transfer_id, dest_chain_id, False)
    return ConnextTransfer(transfer_id, origin_txn, dest_txn)
