from typing import Optional

from .array_info import ArrayInfo
from .containers.dir import Dir
from .utils.types import MemoryAddress
from .var_info import VarInfo


class VarTable(Dir[VarInfo]):
    def __init__(self) -> None:
        super().__init__()

    def add(
        self,
        name: str,
        var_type: str,
        address: MemoryAddress = 0,
        array_info: Optional[ArrayInfo] = None,
    ) -> VarInfo:
        """
        Insert a new variable to the table.

        Arguments:
        name: str -- Variable name.
        address: MemoryAddress -- Address where the variable is saved.
        array_info: Optional[ArrayInfo] = None -- Information corresponding to array size and dimensions if the variable is an array.
        """
        if name in self.dir:
            raise Exception(f"The variable {name} is already in the table.")
        else:
            self.dir[name] = VarInfo(name, var_type, address, array_info)
        return self.dir[name]

    def get_from_address(self, address: MemoryAddress) -> VarInfo:
        """
        Get a variable in the table.

        Arguments:
        address: MemoryAddress -- Address where the variable is saved.
        """
        for var_info in self.dir.values():
            if var_info.address == address:
                return var_info
        raise Exception(f"Can't retrieve variable with address {address}.")

    def __str__(self) -> str:
        """
        Stringify every item of the table for readability.
        """
        var_string = ""
        for key, value in self.dir.items():
            var_string += f"<var_name:{key},var_info:{value}>\n"
        return var_string

    def print(self, table_name: str, verbose: bool) -> None:
        """
        Print information of the table depending on verbose flag value.
        """
        if verbose:
            print(f"# {table_name}")
            var_string_list = self.__str__().split("\n")
            for value in var_string_list:
                print(f"# {value}")
