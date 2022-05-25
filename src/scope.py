from .memory import Memory
from .var_table import VarTable
from .utils.types import TypeAddress
from .utils.enums import Types, ScopeTypes


class Scope:
    mem: Memory
    type: ScopeTypes
    var_table: VarTable

    def __init__(self, type: ScopeTypes, mem: Memory) -> None:
        self.mem = mem
        self.type = type
        self.var_table = VarTable()

    def has(self, var_name: str) -> bool:
        return self.var_table.has(var_name)

    def get(self, var_name: str) -> TypeAddress:
        var_info = self.var_table.get(var_name)
        return var_info["type"], var_info["address"], var_info["name"]

    def add(self, var_name: str, var_type: Types) -> TypeAddress:
        var_info = self.var_table.add(var_name, var_type, self.mem.reserve(var_type))
        return var_info["type"], var_info["address"], var_info["name"]