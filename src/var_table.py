from .array_info import ArrayInfo
from .utils.enums import Types
from .utils.types import MemoryAddress
from .var_info import VarInfo


class VarTable:
    table: dict[str, VarInfo]

    def __init__(self) -> None:
        self.table = {}

    def add(
        self, name: str, var_type: Types, address: MemoryAddress, array_info: ArrayInfo
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

    def print(self, table_name: str, verbose: bool) -> None:
        """
        Print the VarTable
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
