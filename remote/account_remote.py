from model import Account
from requests import get
from .setup import get_handler, to_checksum_address
from .transaction_remote import parse_transaction_json
import util

WEI_TO_ETH = 1e18
handler = get_handler()
DUMMY_ACCOUNT = Account("0x0000000000000000000000000000000000000000", 0, False, -1)


def get_account_info_from_remote(query_address, chain_id):
    query_url = util.QUERY_ACCOUNT_URL_TEMPLATE.format(util.CHAINSCAN_URL[chain_id], "balance", query_address, util.CHAINSCAN_API[chain_id])
    response = get(query_url)
    if response.status_code != 200 or not util.is_valid_data(response.json()): return DUMMY_ACCOUNT
    data = response.json()
    return Account(query_address, data["result"], handler.get_code(to_checksum_address(query_address.strip())).hex() != '0x', chain_id)


def get_normal_transaction_from_account(query_address, chain_id, not_internal=True):
    query_url = util.QUERY_ACCOUNT_URL_TEMPLATE.format(util.CHAINSCAN_URL[chain_id], "txlist" if not_internal else "txlistinternal", query_address, util.CHAINSCAN_API[chain_id]) + util.QUERY_INFO
    response = get(query_url)
    if response.status_code != 200 or not util.is_valid_data(response.json()): return []
    data, normal_txns = response.json(), []
    for txn_json in data["result"]: normal_txns.append(parse_transaction_json(txn_json, data["status"], chain_id))
    return normal_txns
