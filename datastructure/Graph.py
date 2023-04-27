import in_mem
from model import Account, Transaction

INITIAL_SIZE = int(1e6)


class Graph:
    def __init__(self):
        self._vertices = []
        self._edges = []
        self._vertex_count = 0
        self._heads = [None] * INITIAL_SIZE
        self._nexts = [None] * INITIAL_SIZE
        self._vers = [None] * INITIAL_SIZE
        self._edge_count = 0
        self._account_vertex_id_map = {}
        self._txn_edge_id_map = {}

    def _add(self, vertex_idx1, vertex_idx2, edge_id):
        self._vers[edge_id] = vertex_idx2
        self._nexts[edge_id] = self._heads[vertex_idx1]
        self._heads[vertex_idx1] = edge_id

    def add_vertex_account(self, account: Account):
        if account.address in self._account_vertex_id_map.keys(): return
        self._account_vertex_id_map[account.address] = self._vertex_count
        self._vertices.append(account.address)
        self._vertex_count += 1

    def get_vertex_account(self, vertex_idx):
        return in_mem.in_mem_account_ids[self._vertices[vertex_idx]]

    def add_edge_transaction(self, account1: Account, account2: Account, txn: Transaction):
        self._txn_edge_id_map[txn.txn_hash] = self._edge_count
        self._edges.append(txn.txn_hash)
        if account1.address not in self._account_vertex_id_map.keys(): self.add_vertex_account(account1)
        if account2.address not in self._account_vertex_id_map.keys(): self.add_vertex_account(account2)
        self._add(self._account_vertex_id_map[account1.address], self._account_vertex_id_map[account2.address], self._txn_edge_id_map[txn.txn_hash])
        self._edge_count += 1

    def __str__(self):
        return f"""Graph:
    --- Number of vertices: {self._vertex_count}
    --- Number of edges: {self._edge_count}
    --- Vertices: {self._vertices}
    --- Transactions: {self._edges}
        """
