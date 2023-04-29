from collections import namedtuple
from functools import reduce
import json
from typing import List, Dict


class Contract:
    def __init__(self, contract_address, abi_raw, chain_id):
        self.contract_address: str = contract_address
        self.abi_raw: str = abi_raw
        self.chain_id = chain_id
        self.constructor: Constructor = None
        self.events: List[Event] = None
        self.functions: List[Function] = None
        self._parse_abi_raw()

    def __str__(self):
        return f"""Contract at address {self.contract_address}:
        
                    {self.constructor}
                    {self.chain_id}
                    {reduce(lambda prv, cur: prv + str(cur), self.events, "")}
                    {reduce(lambda prv, cur: prv + str(cur), self.functions, "")}
        """

    def _parse_abi_raw(self,):
        abi_json = json.loads(self.abi_raw.replace("\\\"", "\""))
        constructor_json = next(filter(lambda elem: elem["type"] == "constructor", abi_json))
        self.constructor = Constructor(constructor_json["inputs"], constructor_json["stateMutability"])
        event_jsons = list(filter(lambda elem: elem["type"] == "event", abi_json))
        self.events = list(map(lambda jsn: Event(jsn["anonymous"], jsn["inputs"], jsn["name"]), event_jsons))
        func_jsons = list(filter(lambda elem: elem["type"] == "function", abi_json))
        self.functions = list(map(lambda jsn: Function(jsn["inputs"], jsn["name"], jsn["outputs"], jsn["stateMutability"]), func_jsons))


NameTypeTuple = namedtuple("NameTypeTuple", ["internal_type", "name", "type"])
IndexedNameTypeTuple = namedtuple("IndexedNameTypeTuple", ["indexed", "internal_type", "name", "type"])
map_name_type_tuple = lambda jsn: NameTypeTuple(jsn["internalType"] if "internalType" in jsn else None, jsn["name"], jsn["type"])
map_indexed_name_type_tuple = lambda jsn: IndexedNameTypeTuple(jsn["indexed"], jsn["internalType"] if "internalType" in jsn else None, jsn["name"], jsn["type"])


class Constructor:
    def __init__(self, inputs, state_mutability):
        self.inputs = list(map(map_name_type_tuple, inputs))
        self.state_mutability = state_mutability

    def __str__(self):
        return f"""Constructor:
                    - Inputs: {self.inputs}
                    - State mutability: {self.state_mutability}
        
        """

class Event:
    def __init__(self, anonymous, inputs, name):
        self.anonymous = anonymous
        self.inputs = list(map(map_indexed_name_type_tuple, inputs))
        self.name = name

    def __str__(self):
        return f"""Event:
                    - Anonymous: {self.anonymous}
                    - Inputs: {self.inputs}
                    - Name: {self.name}
        
        """


class Function:
    def __init__(self, inputs, name, outputs, state_mutability):
        self.inputs = list(map(map_name_type_tuple, inputs))
        self.name = name
        self.outputs = list(map(map_name_type_tuple, outputs))
        self.state_mutability = state_mutability

    def __str__(self):
        return f"""Function:
                    - Inputs: {self.inputs}
                    - Name: {self.name}
                    - Outputs: {self.outputs}
                    - State mutability: {self.state_mutability}
        
        """




