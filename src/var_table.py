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

    def __del__(self) -> None:
        del self.table
