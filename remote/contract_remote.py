import time
import aiohttp
from model import Contract
from requests import get
from .setup import get_handler, to_checksum_address
from typing import Dict, List, Union
import util

handler = get_handler()
GET_SMART_CONTRACT_ABI_QUERY = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey={}"


T20_PROPERTY = {
    "functions": [
        "0x06fdde03",   # name()
        "0x95d89b41",   # symbol()
        "0x313ce567",   # decimals()
        "0x18160ddd",   # totalSupply()
        "0x70a08231",   # balanceOf(address)
        "0xa9059cbb",   # transfer(address,uint256)
        "0x23b872dd",   # transferFrom(address,address,uint256)
        "0x095ea7b3",   # approve(address,uint256)
        "0xdd62ed3e",   # allowance(address,address)
    ],
    "events": [
        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",   # Transfer(address,address,uint256)
        "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"    # Approval(address,address,uint256)

    ]
}


async def get_smart_contract_abi_format(contract_address, chain_id):
    query = GET_SMART_CONTRACT_ABI_QUERY.format(contract_address, util.CHAINSCAN_API[chain_id])
    async with aiohttp.ClientSession() as session:
        async with session.get(query) as response:
            result = await response.json()
    result = result["result"]
    while result == "Max rate limit reached": time.sleep(0.1); result = get(query).json()["result"]
    return result


async def construct_smart_contract_object(contract_address, chain_id):
    abi_raw = await get_smart_contract_abi_format(contract_address, chain_id)
    return Contract(contract_address, abi_raw, chain_id)


def is_t20_smart_contract_(contract: Contract):
    if contract.functions is None or contract.events is None: return False
    all_funcs_id, all_events_id = contract.functions.keys(), contract.events.keys()
    return all(fn_id in all_funcs_id for fn_id in T20_PROPERTY["functions"]) and all(evt_id in all_events_id for evt_id in T20_PROPERTY["events"])


async def is_t20_smart_contract(contract_address, chain_id):
    contract = await construct_smart_contract_object(contract_address, chain_id)
    return is_t20_smart_contract_(contract)


async def invoke_smart_contract_function(contract_address, queries_abi: List[Dict[str, Union[str, List, Dict]]]):
    contract = handler.contract(address=to_checksum_address(contract_address), abi=queries_abi)
    result = list(map(lambda abi: getattr(contract.functions, abi["name"])().call(), queries_abi))
    return [await cr for cr in result]
