#
# @file func_directory.py
# @author David Luna and Yulisa Medina
# @brief
# @version 0.1
# @date 2022-05-05
#
# @copyright Copyright (c) 2022
#
#

from typing import TypedDict, Union

from .var_table import VarTable
from .utils.types import FunctionResources


class FuncInfo(TypedDict):
    type: str
    var_table: VarTable
    param_table: VarTable
    resources: FunctionResources
    start_quad: int | None


class FuncDir:
    func_dir: dict[str, FuncInfo]

    def __init__(self):
        self.func_dir = {}

    def add(self, name: str, return_type: str) -> None:
        """
        Insert a new function to the directory.

        Arguments:
        name: str -- Name of the function.
        return_type: str -- Return type of the function.
        """
        if name in self.func_dir:
            raise Exception(f"The function {name} is already in the directory.")
        else:
            self.func_dir[name] = {
                "type": return_type,
                "var_table": VarTable(),
                "param_table": VarTable(),
                "resources": None,
                "start_quad": None,
            }

    def get(self, name: str) -> Union[FuncInfo, None]:
        """
        Get a function in the directory.

        Arguments:
        name: str -- Name of the function.

        Returns
        Union[FuncInfo, None] -- None, if the function is not found.
        """
        return self.func_dir.get(name)

    def has(self, name: str) -> bool:
        """
        Check whether a function is contained in the directory.

        Arguments:
        name: str -- Name of the function to check.

        Returns:
        bool: True, if it exists, otherwise, False.
        """
        return False if self.func_dir.get(name) is None else True

    def print(self) -> None:
        """
        Print the function directory.
        """
        for key, value in self.func_dir.items():
            print(f'Function: {key} with return type: {value["type"]}\n')
            print(f'Resources: {value["resources"]}\n')
            print(f'Start quadruple: {value["start_quad"]}\n')
            value["param_table"].print("Parameters table")
            print("\n")
            value["var_table"].print("Variables table")
            print("\n")
