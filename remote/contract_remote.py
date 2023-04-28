from model import Contract
from requests import get
import util

GET_SMART_CONTRACT_ABI_QUERY = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey={}"


def get_smart_contract_abi_format(contract_address):
    query = GET_SMART_CONTRACT_ABI_QUERY.format(contract_address, util.ETHSCAN_API)
    return get(query).json()["result"]


def construct_smart_contract_object(contract_address):
    abi_raw = get_smart_contract_abi_format(contract_address)
    return Contract(contract_address, abi_raw)



