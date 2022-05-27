from typing import Optional

from .array_info import ArrayInfo
from .memory import Memory
from .utils.enums import Types, ScopeTypes
from .utils.types import TypeAddress
from .var_table import VarTable
from .var_info import VarInfo


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

    def get(self, var_name: str) -> VarInfo:
        return self.var_table.get(var_name)

    def add(
        self, var_name: str, var_type: Types, array_info: Optional[ArrayInfo] = None
    ) -> TypeAddress:
        if array_info is None:
            address = self.mem.reserve(var_type)
        else:
            address = self.mem.reserve(var_type, array_info.size)
        var_info = self.var_table.add(var_name, var_type, address, array_info)
        return (var_info.type, var_info.address, var_info.name)
