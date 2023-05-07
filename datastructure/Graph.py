import in_mem
from model import Account, Transaction, TokenTransfer
from typing import List, Union

INITIAL_SIZE = int(1e6)

"""
Edge Type:
-- 0: Transaction
-- 1: T20 (ERC20) Token Transfer
"""


def construct_graph_from_transactions(txn_list: List[Transaction]):
    graph = Graph()
    print(txn_list)
    for txn in txn_list: graph.add_edge_transaction(txn.from_account, txn.to_account, txn)
    return graph


class Graph:
    def __init__(self):
        self._vertices = []
        self._edges: List[List] = []
        self._vertex_count = 0
        self._heads: List[List] = [[None] * INITIAL_SIZE, [None] * INITIAL_SIZE]
        self._nexts: List[List] = [[None] * INITIAL_SIZE, [None] * INITIAL_SIZE]
        self._vers: List[List] = [[None] * INITIAL_SIZE, [None] * INITIAL_SIZE]
        self._edge_count = 0
        self._account_vertex_id_map = {}
        self._relation_edge_id_map = {}

    def _add(self, vertex_idx1, vertex_idx2, edge_id, edge_type):
        self._vers[edge_type][edge_id] = vertex_idx2
        self._nexts[edge_type][edge_id] = self._heads[edge_type][vertex_idx1]
        self._heads[edge_type][vertex_idx1] = edge_id

    def _add_data(self, vertex1, vertex2, edge: Union[Transaction, TokenTransfer], typ):
        if vertex1 not in self._account_vertex_id_map.keys(): self.add_vertex_account(vertex1)
        if vertex2 not in self._account_vertex_id_map.keys(): self.add_vertex_account(vertex2)
        self._relation_edge_id_map[edge.__hash__()] = self._edge_count
        self._edges.append(edge)
        self._edge_count += 1
        self._add(self._account_vertex_id_map[vertex1], self._account_vertex_id_map[vertex2], self._relation_edge_id_map[edge.__hash__()], typ)

    def add_vertex_account(self, account_address):
        if account_address in self._account_vertex_id_map.keys(): return
        self._account_vertex_id_map[account_address] = self._vertex_count
        self._vertices.append(account_address)
        self._vertex_count += 1

    def get_vertex_account(self, vertex_idx):
        return in_mem.in_mem_account_ids[self._vertices[vertex_idx]]

    def add_edge_transaction(self, account1, account2, txn: Transaction):
        self._add_data(account1, account2, txn, 0)
        for transfer in txn.tokens_transferred: self._add_data(transfer.sender, transfer.receiver, transfer, 1)

    def print_self(self):
        print(self.__str__())
        for edge in self._edges: print(edge)

    def __str__(self):
        return f"""Graph:
    --- Number of vertices: {self._vertex_count}
    --- Number of edges: {self._edge_count}
    --- Vertices: {self._vertices}
        """
