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

from typing import TypedDict, Generic, TypeVar
from abc import ABC, abstractmethod

from .memory import Memory
from .scope import Scope
from .utils.enums import Types, ScopeTypes
from .utils.types import FunctionResources, MemoryAddress
from .var_table import VarTable


class CFuncInfo(TypedDict):
    body_defined: bool
    has_return_statement: bool
    param_table: VarTable
    resources: FunctionResources
    return_address: MemoryAddress
    scope: Scope
    start_quad: int | None
    type: Types


class VMFuncInfo(TypedDict):
    start_quad: int
    resources: FunctionResources


T = TypeVar("T", CFuncInfo, VMFuncInfo)


class FuncDir(ABC, Generic[T]):
    func_dir: dict[str, T]

    def __init__(self):
        self.func_dir = {}

    @abstractmethod
    def print(self, verbose: bool) -> None:
        """
        Print the function directory.
        """
        pass

    @abstractmethod
    def add(self) -> T:
        """
        Insert a new function to the directory.
        """
        pass

    def get(self, name: str) -> T:
        """
        Get a function in the directory.
        """
        if (func_info := self.func_dir.get(name)) is not None:
            return func_info
        else:
            raise Exception(f"Couldn't retrieve the information of function {name}.")

    def has(self, name: str) -> bool:
        """
        Check whether a function is contained in the directory.
        """
        return False if self.func_dir.get(name) is None else True


class CFuncDir(FuncDir[CFuncInfo]):
    def __init__(self):
        super().__init__()

    def add(
        self,
        name: str,
        body_defined: bool,
        return_type: Types,
        return_address: MemoryAddress,
        mem: Memory,
    ) -> CFuncInfo:
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

    def print(self, verbose: bool) -> None:
        for key, value in self.func_dir.items():
            if verbose:
                print(f'# Function: {key} with return type: {value["type"]}')
                print(f'# Resources: {value["resources"]}')
                print(f'# Start quadruple: {value["start_quad"]}')
                print(f'# Return address: {value["return_address"]}')
                value["param_table"].print("Parameters table", True)
            print(
                f"{key},{value['start_quad']},{str(value['resources']).removeprefix('(').removesuffix(')')}"
            )


class VMFuncDir(FuncDir[VMFuncInfo]):
    def __init__(self):
        super().__init__()

    def add(
        self,
        name: str,
        start_quad: int,
        resources: FunctionResources,
    ) -> VMFuncInfo:
        if name in self.func_dir:
            raise Exception(f"The function {name} is already in the directory.")
        else:
            self.func_dir[name] = {
                "resources": resources,
                "start_quad": start_quad,
            }
            return self.func_dir[name]

    def print(self, verbose: bool) -> None:
        for key, value in self.func_dir.items():
            if verbose:
                print(f"# Function: {key}")
                print(f'# Resources: {value["resources"]}')
                print(f'# Start quadruple: {value["start_quad"]}')
            else:
                print(
                    f"# {key},{value['start_quad']},{str(value['resources']).removeprefix('(').removesuffix(')')}"
                )
