from model import Account
from requests import get
from transactionRemote import parse_transaction_json
import util

WEI_TO_ETH = 1e18
ACCOUNT_URL_TEMPLATE = util.BASE_ETHSCAN_URL + "?module=account&action={}&address={}&tag=latest&apikey={}"
NORM_TXN_QUERY = "&startblock=0&endblock=99999999&page=1&offset=10&sort=asc"


def get_account_info_from_remote(query_address):
    query_url = ACCOUNT_URL_TEMPLATE.format("balance", query_address, util.ETHSCAN_API)
    data = get(query_url).json()
    return Account(query_address, data["result"])


def get_normal_transaction_from_account(query_address, net="Ethereum"):
    query_url = ACCOUNT_URL_TEMPLATE.format("txlist", query_address, util.ETHSCAN_API) + NORM_TXN_QUERY
    data = get(query_url).json()
    normal_txns = []
    for txn_json in data["result"]: normal_txns.append(parse_transaction_json(txn_json, data["status"], net))
    return normal_txns
