from typing import Optional

from .array_info import ArrayInfo
from .utils.types import MemoryAddress
from .var_info import VarInfo


class VarTable:
    table: dict[str, VarInfo]

    def __init__(self) -> None:
        self.table = {}

    def add(
        self,
        name: str,
        var_type: str,
        address: Optional[MemoryAddress] = None,
        array_info: Optional[ArrayInfo] = None,
    ) -> VarInfo:
        """
        Insert a new variable to the table.
        """
        if name in self.table:
            raise Exception(f"The variable {name} is already in the table.")
        else:
            self.table[name] = VarInfo(name, var_type, address, array_info)
        return self.table[name]

    def get(self, name: str) -> VarInfo:
        """
        Get a variable in the table.
        """
        if (var_info := self.table.get(name)) is not None:
            return var_info
        else:
            raise Exception(f"Can't retrieve variable with name {name}.")

    def get_from_address(self, address: MemoryAddress) -> VarInfo:
        """
        Get a variable in the table.
        """
        for var_info in self.table.values():
            if var_info.address == address:
                return var_info
        raise Exception(f"Can't retrieve variable with address {address}.")

    def has(self, name: str) -> bool:
        """
        Check whether a variable is contained in the table.
        """
        return False if self.table.get(name) is None else True

    def __str__(self) -> str:
        var_string = ""
        for key, value in self.table.items():
            var_string += f"<var_name:{key},var_info:{value}>\n"
        return var_string

    def print(self, table_name: str, verbose: bool) -> None:
        """
        Print the VarTable
        """
        if verbose:
            print(f"# {table_name}")
            var_string_list = self.__str__().split("\n")
            for value in var_string_list:
                print(f"# {value}")
