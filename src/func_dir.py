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

from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from .scope import Scope
from .utils.enums import Types
from .utils.types import FunctionResources, MemoryAddress, ParamList


class FuncInfo:
    start_quad: int
    resources: FunctionResources
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class CFuncInfo(FuncInfo):
    address: MemoryAddress
    has_return: bool
    is_body_defined: bool
    param_list: ParamList
    return_address: MemoryAddress | None
    scope: Scope
    type: Types

    def __init__(
        self,
        name: str,
        return_address: MemoryAddress | None,
        scope: Scope,
        type: Types,
        address: MemoryAddress,
    ) -> None:
        super().__init__(name)
        self.address = address
        self.has_return = False
        self.is_body_defined = False
        self.param_list = []
        self.resources = (0, 0, 0, 0, 0)
        self.return_address = return_address
        self.scope = scope
        self.type = type


class VMFuncInfo(FuncInfo):
    def __init__(
        self,
        name: str,
        start_quad: int,
        resources: FunctionResources,
    ) -> None:
        super().__init__(name)
        self.start_quad = start_quad
        self.resources = resources


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
        return_type: Types,
        return_address: MemoryAddress | None,
        scope: Scope,
        address: MemoryAddress,
    ) -> CFuncInfo:
        if name in self.func_dir and self.func_dir[name].is_body_defined:
            raise Exception(f"The function {name} is already in the directory.")
        else:
            self.func_dir[name] = CFuncInfo(
                name, return_address, scope, return_type, address
            )
            return self.func_dir[name]

    def print(self, verbose: bool) -> None:
        for key, value in self.func_dir.items():
            if verbose:
                print(f"# Function: {key} with return type: {value.type}")
                print(f"# Resources: {value.resources}")
                print(f"# Start quadruple: {value.start_quad}")
                print(f"# Return address: {value.return_address}")
                print(f"# Parameters list: {[param for param in value.param_list]}")
                print(f"# Address: {value.address}")
            print(
                f"{key},{value.start_quad},{str(value.resources).removeprefix('(').removesuffix(')')}"
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
            self.func_dir[name] = VMFuncInfo(name, start_quad, resources)
            return self.func_dir[name]

    def print(self, verbose: bool) -> None:
        for key, value in self.func_dir.items():
            if verbose:
                print(f"# Function: {key}")
                print(f"# Resources: {value.resources}")
                print(f"# Start quadruple: {value.start_quad}")
            else:
                print(
                    f"# {key},{value.start_quad},{str(value.resources).removeprefix('(').removesuffix(')')}"
                )
