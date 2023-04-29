import datetime
import json

SUPPORT_CHAIN_ID = [1, 10, 56, 100, 137, 42161]


# API Information
INFURA_API = "cd88aac309b94a13b33f1b90874ae28e"
ETHSCAN_API = "AVH9VRH4PNFSGF6V8RXEXDZ19R5RGUMBU9"
POLYGONSCAN_API = "NPFNK3NCWZM3XPJGFB7AFABR4GDSNNPKDN"
BSCSCAN_API = "2UCYK12HBHXTNR65ZSU5QFGKHK8QDMAEK4"
ARBISCAN_API = "187YD9ZG38JFS4PX2I4ATAH94HJZVGD8AP"
OPTIMISIMSCAN_API = "GDGJFWFSR47SN3S4KTBPWBRACZI8E9PXGS"
GNOSISSCAN_API = "GBNY7156AE9CDIYWU5YDQ1AMGHXC7HGE2R"

CHAINSCAN_API = {
    1: ETHSCAN_API,
    10: OPTIMISIMSCAN_API,
    56: BSCSCAN_API,
    100: GNOSISSCAN_API,
    137: POLYGONSCAN_API,
    42161: ARBISCAN_API
}


# Infrastructure
INFURA_PROVIDER = "https://mainnet.infura.io/v3/{}".format(INFURA_API)
BASE_ETHSCAN_URL = "https://api.etherscan.io/api"
BASE_OPTIMISMSCAN_URL = "https://api-optimistic.etherscan.io/api"
BASE_BSCSCAN_URL = "https://api.bscscan.com/api"
BASE_GNOSISSCAN_URL = "https://api.gnosisscan.io/api"
BASE_POLYGONSCAN_URL = "https://api.polygonscan.com/api"
BASE_ARBISCAN_URL = "https://api.arbiscan.io/api"

CHAINSCAN_URL = {
    1: BASE_ETHSCAN_URL,
    10: BASE_OPTIMISMSCAN_URL,
    56: BASE_BSCSCAN_URL,
    100: BASE_GNOSISSCAN_URL,
    137: BASE_POLYGONSCAN_URL,
    42161: BASE_ARBISCAN_URL
}


# Project Specific Information
CONNEXT_TRANSFER_API = "https://postgrest.mainnet.connext.ninja/transfers?transfer_id=eq.{}"
CONNEXT_GRAPH_API = "https://gateway.thegraph.com/api/a139ff34a0d410cd9267dc13bace6659/subgraphs/id/DfD1tZSmDtjCGC2LeYEQbVzj9j8kNqKAQEsYL27Vg6Sw"

CONNEXT_ETHEREUM_CONTRACT = "0x8898B472C54c31894e3B9bb83cEA802a5d0e63C6 "
CONNEXT_OPTIMISM_CONTRACT = "0x5bb83e95f63217cda6ae3d181ba580ef377d2109"
CONNEXT_BSC_CONTRACT = "0xCd401c10afa37d641d2F594852DA94C700e4F2CE"
CONNEXT_GNOSIS_CONTRACT = "0x5bb83e95f63217cda6ae3d181ba580ef377d2109"
CONNEXT_POLYGON_CONTRACT = "0x11984dc4465481512eb5b777e44061c158cf2259"
CONNEXT_ARBITRUM_CONTRACT = "0x1231deb6f5749ef6ce6943a275a1d3e7486f4eae"

CONNEXT_CONTRACT_ADDRESS = {
    1: CONNEXT_ETHEREUM_CONTRACT,
    10: CONNEXT_OPTIMISM_CONTRACT,
    56: CONNEXT_BSC_CONTRACT,
    100: CONNEXT_GNOSIS_CONTRACT,
    137: CONNEXT_POLYGON_CONTRACT,
    42161: CONNEXT_ARBITRUM_CONTRACT
}


def convert_linux_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")


def is_valid_json(message):
    try: json.loads(json.dumps(message))
    except ValueError as e: return False
    return True


def is_valid_data(data):
    return is_valid_json(data) and data["message"] != "NOTOK" and "Max rate limit reached" not in str(data)
