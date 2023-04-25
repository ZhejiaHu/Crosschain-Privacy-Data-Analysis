import datetime
import json

INFURA_API = "cd88aac309b94a13b33f1b90874ae28e"
INFURA_PROVIDER = "https://mainnet.infura.io/v3/{}".format(INFURA_API)
ETHSCAN_API = "AVH9VRH4PNFSGF6V8RXEXDZ19R5RGUMBU9"
BASE_ETHSCAN_URL = "https://api.etherscan.io/api"


def convert_linux_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")


def is_valid_json(message):
    try: json.loads(json.dumps(message))
    except ValueError as e: return False
    return True


def is_valid_data(data):
    return is_valid_json(data) and data["message"] != "NOTOK" and "Max rate limit reached" not in str(data)
