from typing import TypedDict

from .array_info import ArrayInfo
from .utils.enums import Types
from .utils.types import MemoryAddress


class VarInfo(TypedDict):
    name: str
    type: Types
    address: MemoryAddress
    array_info: ArrayInfo


class VarTable:
    table: dict[str, VarInfo]

    def __init__(self) -> None:
        self.table = {}

    def add(
        self, name: str, var_type: Types, address: MemoryAddress, array_info: ArrayInfo
    ) -> VarInfo:
        """
        Insert a new variable to the table.

        Arguments:
        name: str -- Name of the variable.
        var_type: str -- Type of the variable.
        address: MemoryAddress -- Address of the variable.
        """
        if name in self.table:
            raise Exception(f"The variable {name} is already in the table.")
        else:
            self.table[name] = {
                "name": name,
                "type": var_type,
                "address": address,
                "array_info": array_info,
            }
            return self.table[name]

    def get(self, name: str) -> VarInfo:
        """
        Get a variable in the table.

        Arguments:
        name: str -- Variable to get.

        Returns:
        VarInfo -- Information about the variable.
        """
        if (var_info := self.table[name]) is not None:
            return var_info
        else:
            raise Exception(f"Can't retrieve variable with name {name}.")

    def get_from_address(self, address: MemoryAddress) -> VarInfo:
        """
        Get a variable in the table.

        Arguments:
        addr: MemoryAddress -- Variable to get.

        Returns:
        VarInfo -- Information about the variable.
        """
        for k, v in self.table.items():
            if v["address"] == address:
                return v
        raise Exception(f"Can't retrieve variable with address {address}.")

    def has(self, name: str) -> bool:
        """
        Check whether a variable is contained in the table.

        Arguments:
        name: str -- Name of the variable to check.

        Returns:
        bool: True, if it exists, otherwise, False.
        """
        return False if self.table.get(name) is None else True

    def print(self, table_name: str, verbose: bool) -> None:
        """
        Print the VarTable

        Arguments:
        table_name: str -- Name to print in the table header.
        """
        # TODO: Look for a better printing method. This thing is UGLY!
        char_length = 100
        column_lenght = (char_length - 5) / 4
        template_string = f"|{{:^{column_lenght}}}|{{:^{column_lenght}}}|{{:^{column_lenght}}}|{{:^{char_length - column_lenght * 3 - 2}}}|"
        bar = "".join(["-" * char_length])
        template_header = f"|{{:^{char_length - 2}}}|"
        if verbose:
            print(f"# {bar}")
            print(f"# {template_header.format(table_name)}")
            print(f"# {bar}")
            print(
                f'# {template_string.format("Variable name", "Type", "Name", "Address")}'
            )
            if len(self.table.items()) > 0:
                for key, value in self.table.items():
                    print(
                        f'# { template_string.format( key, value["type"], value["name"], str(value["address"]))}'
                    )
            print(f"# {bar}")
