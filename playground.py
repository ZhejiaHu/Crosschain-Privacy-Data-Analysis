import asyncio
from remote import construct_graph_from_latest_block
"""
    07/05/2023: An initial attempt to construct graph from latest block, in asynchronous way
    
"""


async def main():
    graph = await construct_graph_from_latest_block()
    graph.print_self()


if __name__ == "__main__":
    asyncio.run(main())






