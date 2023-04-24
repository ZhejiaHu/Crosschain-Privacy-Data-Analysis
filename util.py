import datetime
import json

ETHSCAN_API = "AVH9VRH4PNFSGF6V8RXEXDZ19R5RGUMBU9"
BASE_ETHSCAN_URL = "https://api.etherscan.io/api"


def convert_linux_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")


def is_valid_json(message):
    try: json.loads(json.dumps(message))
    except ValueError as e: return False
    return True
