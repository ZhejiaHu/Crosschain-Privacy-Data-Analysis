from model import Contract
from requests import get
import util

GET_SMART_CONTRACT_ABI_QUERY = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey={}"


def get_smart_contract_abi_format(contract_address, chain_id):
    query = GET_SMART_CONTRACT_ABI_QUERY.format(contract_address, util.CHAINSCAN_API[chain_id])
    return get(query).json()["result"]


def construct_smart_contract_object(contract_address, chain_id):
    abi_raw = get_smart_contract_abi_format(contract_address, chain_id)
    return Contract(contract_address, abi_raw, chain_id)



