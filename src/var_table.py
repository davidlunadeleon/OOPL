from typing import Any, TypedDict, Union


class VarInfo(TypedDict):
    name: str
    type: str
    value: Any


class VarTable:
    table: dict[str, VarInfo]

    def __init__(self) -> None:
        self.table = {}

    def add(self, name: str, var_type: str, value: Any) -> None:
        """
        Insert a new variable to the table.

        Arguments:
        name: str -- Name of the variable.
        var_type: str -- Type of the variable.
        value: Any -- Value of the variable
        """
        if name in self.table:
            raise Exception(f"The variable {name} is already in the table.")
        else:
            self.table[name] = {
                "name": name,
                "type": var_type,
                "value": value,
            }

    def get(self, name: str) -> Union[VarInfo, None]:
        """
        Get a variable in the table.

        Arguments:
        name: str -- Variable to get.

        Returns:
        Union[VarInfo, None] -- None, if the variable is not found.
        """
        return self.table.get(name)

    def has(self, name: str) -> bool:
        """
        Check whether a variable is contained in the table.

        Arguments:
        name: str -- Name of the variable to check.

        Returns:
        bool: True, if it exists, otherwise, False.
        """
        return False if self.table.get(name) is None else True

    def print(self, table_name: str) -> None:
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
        print(bar)
        print(template_header.format(table_name))
        print(bar)
        print(template_string.format("Variable name", "Type", "Name", "Value"))
        if len(self.table.items()) > 0:
            for key, value in self.table.items():
                print(
                    template_string.format(
                        key, value["type"], value["name"], value["value"]
                    )
                )
        print(bar)
