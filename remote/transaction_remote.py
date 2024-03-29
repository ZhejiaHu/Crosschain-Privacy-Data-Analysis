import asyncio

from model import Transaction, MethodInvocation, TokenTransfer, TokenType, EventLog
from requests import get
from remote.setup import get_handler
from remote.contract_remote import construct_smart_contract_object, is_t20_smart_contract_, T20_PROPERTY, \
    invoke_smart_contract_function
from sha3 import keccak_256
import util

handler = get_handler()
INTERNAL_TXN_HASH = "OxFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"


def _get_basic_information_query_template(item):  # query item belongs to {name, symbol, decimals}
    return {
        "inputs": [],
        "name": item,
        "outputs": [{"internalType": "string" if item != "decimals" else "uint8", "name": "",
                     "type": "string" if item != "decimals" else "uint8"}],
        "stateMutability": "view",
        "type": "function"
    }


async def parse_transaction_json(txn_json, status, chain_id, not_internal=True):
    #internal_txns = get_internal_transaction_from_transaction_hash(txn_json["hash"] if not_internal else INTERNAL_TXN_HASH, chain_id) if not_internal else []
    method_called = MethodInvocation(txn_json["hash"], txn_json["to"], txn_json["methodId"],
                                     txn_json["input"]) if "methodId" in txn_json.keys() and txn_json[
        "methodId"] != "0x" else None
    # tokens = get_token_swap_from_transaction_hash(txn_json["hash"], txn_json["blockNumber"], txn_json["from"], chain_id, TokenType.T20) if not_internal else [] + \
    events_emitted = get_event_log_from_transaction_hash(txn_json["hash"], chain_id)
    return Transaction(txn_json["hash"] if not_internal else INTERNAL_TXN_HASH, status,
                       txn_json["timeStamp"],
                       txn_json["from"],
                       txn_json["to"],
                       txn_json["value"],
                       txn_json["gas"],
                       chain_id,
                       txn_json["blockNumber"],
                       internal_txns=[],
                       method_invoked=method_called,
                       events_emitted=await events_emitted)


async def get_transaction_from_transaction_hash(txn_hash, chain_id=1):
    print(f"Currently getting transaction {txn_hash}.")
    metadata, receipt = await handler.get_transaction(txn_hash), await handler.get_transaction_receipt(txn_hash)
    return Transaction(txn_hash,
                       receipt.status,
                       (await handler.get_block(metadata.blockNumber)).timestamp,
                       metadata["from"],
                       metadata.to,
                       metadata.blockNumber,
                       metadata.value,
                       metadata.gas,
                       chain_id,
                       tokens_transferred=await get_token_transfer_from_transaction_hash(txn_hash, chain_id))


def get_internal_transaction_from_transaction_hash(txn_hash, chain_id):
    query = util.QUERY_TXN_URL_TEMPLATE.format(util.CHAINSCAN_URL[int(chain_id)], "txlistinternal", txn_hash,
                                               util.CHAINSCAN_API[int(chain_id)])
    response = get(query)
    if response.status_code != 200 or not util.is_valid_data(response.json()): return []
    inter_txns = []
    for txn_json in response.json()["result"]: inter_txns.append(
        parse_transaction_json(txn_json, response.json()["status"], chain_id, not_internal=False))
    return inter_txns


def get_token_swap_from_transaction_hash(txn_hash, block_num, initial_account, chain_id, token_type: TokenType):
    account_visited = set()

    def depth_first_search(from_account):
        account_visited.add(from_account)
        action = "tokentx" if token_type == TokenType.T20 else "tokennfttx"
        query = util.QUERY_ACCOUNT_URL_TEMPLATE.format(util.CHAINSCAN_URL[chain_id], action, from_account,
                                                       util.CHAINSCAN_API[chain_id]) + util.QUERY_INFO.format(block_num,
                                                                                                              block_num)
        response = get(query)
        if response.status_code != 200 or not util.is_valid_data(response.json()): return []
        map_to_token_receiver = lambda jsn: (
        TokenTransfer(token_type, jsn["tokenName"], jsn["tokenSymbol"], jsn["tokenDecimal"],
                      jsn["tokenID"] if "tokenID" in jsn else None, jsn["value"] if "value" in jsn else None, txn_hash,
                      jsn["from"], jsn["to"]), jsn["to"])
        filter_token = lambda jsn: jsn["hash"] == txn_hash
        current_token_transfers_ = list(map(map_to_token_receiver, filter(filter_token, response.json()["result"])))
        current_token_transfers, receivers = list(map(lambda tr: tr[0], current_token_transfers_)), set(
            map(lambda tr: tr[1], current_token_transfers_))
        for receiver in receivers:
            if receiver in account_visited: continue
            current_token_transfers.extend(depth_first_search(receiver))
        return current_token_transfers

    return set(depth_first_search(initial_account))


async def get_transactions_from_latest_block(chain_id):
    latest_txn_hashes = await handler.get_block(handler.get_block_number())["transactions"]
    latest_txn_hashes = latest_txn_hashes[:50]  # would be commented out later
    print(len(latest_txn_hashes))
    return list(map(lambda th: get_transaction_from_transaction_hash(th.hex(), chain_id), latest_txn_hashes))


async def get_event_log_from_transaction_hash(txn_hash, chain_id):
    tmp = await handler.get_transaction_receipt(txn_hash)
    logs = tmp.logs
    return list(map(lambda log: EventLog(log["logIndex"], log["address"], list(map(lambda hx: hx.hex(), log["topics"])),
                                         log["data"].hex(), txn_hash, chain_id), logs))


async def is_transfer_t20_token_event_log(event_log: EventLog, chain_id):
    contract_address = event_log.contract_address
    contract = await construct_smart_contract_object(contract_address, chain_id)
    if not is_t20_smart_contract_(contract): return False
    print(f"Index {event_log.event_idx} passes basic test.")
    return event_log.topics[0] == T20_PROPERTY["events"][0]


async def get_token_transfer_from_transaction_hash_(txn_hash, chain_id=1):
    events_emitted = await get_event_log_from_transaction_hash(txn_hash, chain_id)
    transfer_t20_events = []
    for evt in events_emitted:
        test = await is_transfer_t20_token_event_log(evt, chain_id)
        if test: transfer_t20_events.append(evt)
    return transfer_t20_events


def _parse_account_address_from_topic(topic_repr):
    return "0x" + topic_repr[-40:]


async def decode_token_transfer_from_event_t20(txn_hash, event_log: EventLog):
    contract_address, queries_abi = event_log.contract_address, [_get_basic_information_query_template(item) for item in ["name", "symbol", "decimals"]]
    results = await invoke_smart_contract_function(contract_address, queries_abi)
    return TokenTransfer(TokenType.T20,
                         results[0],
                         results[1],
                         results[2],
                         -1,
                         event_log.data,
                         txn_hash,
                         _parse_account_address_from_topic(event_log.topics[1]),
                         _parse_account_address_from_topic(event_log.topics[2]))


async def get_token_transfer_from_transaction_hash(txn_hash, chain_id=1):
    # target_txn: Transaction = get_transaction_from_transaction_hash(txn_hash, chain_id)
    token_transfer_event_logs = await get_token_transfer_from_transaction_hash_(txn_hash, chain_id)
    result = list(map(lambda pr: decode_token_transfer_from_event_t20(pr[0], pr[1]), zip([txn_hash] * len(token_transfer_event_logs), token_transfer_event_logs)))
    return [await cr for cr in result]


async def get_transaction_from_transaction_hash_multiprocess_async_(txn_hash, chain_id=1):
    txn = await get_transaction_from_transaction_hash(txn_hash, chain_id)
    return txn


def get_transaction_from_transaction_hash_multiprocess_async(txn_hash, storage, idx, chain_id=1, ):  # pair[0] is the function and pair[1] is the arguments
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_transaction_from_transaction_hash_multiprocess_async_(txn_hash, chain_id))
    storage[idx] = result

