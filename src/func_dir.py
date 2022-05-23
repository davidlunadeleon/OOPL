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

from .memory import Memory
from .scope import Scope
from .utils.enums import Types, ScopeTypes
from .utils.types import FunctionResources, MemoryAddress
from .var_table import VarTable


class FuncInfo(TypedDict):
    body_defined: bool
    has_return_statement: bool
    param_table: VarTable
    resources: FunctionResources
    return_address: MemoryAddress
    scope: Scope
    start_quad: int | None
    type: Types


class FuncDir:
    func_dir: dict[str, FuncInfo]

    def __init__(self):
        self.func_dir = {}

    def add(
        self,
        name: str,
        body_defined: bool,
        return_type: Types,
        return_address: MemoryAddress,
        mem: Memory,
    ) -> FuncInfo:
        """
        Insert a new function to the directory.

        Arguments:
        name: str -- Name of the function.
        body_defined: bool -- Whether the function body was registered before (for header definition control).
        return_type: str -- Return type of the function.
        """
        if name in self.func_dir and self.func_dir[name]["body_defined"]:
            raise Exception(f"The function {name} is already in the directory.")
        else:
            self.func_dir[name] = {
                "body_defined": body_defined,
                "has_return_statement": False,
                "param_table": VarTable(),
                "resources": (0, 0, 0, 0),
                "return_address": return_address,
                "scope": Scope(ScopeTypes.FUNCTION, mem),
                "start_quad": None,
                "type": return_type,
            }
            return self.func_dir[name]

    def get(self, name: str) -> FuncInfo:
        """
        Get a function in the directory.

        Arguments:
        name: str -- Name of the function.

        Returns
        FuncInfo -- Information about the function.
        """
        if (func_info := self.func_dir.get(name)) is not None:
            return func_info
        else:
            raise Exception(f"Couldn't retrieve the information of function {name}.")

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
            print(f'Return address: {value["return_address"]}\n')
            value["param_table"].print("Parameters table")
            print("\n")
