import web3

from util import INFURA_PROVIDER
from web3 import AsyncWeb3, AsyncHTTPProvider

handler = AsyncWeb3(AsyncHTTPProvider(INFURA_PROVIDER))


def get_handler():
    global handler
    return handler.eth


def to_checksum_address(address):
    return handler.to_checksum_address(address)
