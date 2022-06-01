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

from .func_info import CFuncInfo, VMFuncInfo
from .scope import Scope
from .utils.types import Resources, MemoryAddress
from .containers.dir import Dir


class CFuncDir(Dir[CFuncInfo]):
    def __init__(self) -> None:
        super().__init__()

    def add(
        self,
        name: str,
        return_type: str,
        return_address: MemoryAddress,
        scope: Scope,
        address: MemoryAddress,
    ) -> CFuncInfo:
        if self.has(name) and self.get(name).is_body_defined:
            raise Exception(f"The function {name} is already in the directory.")
        else:
            self.dir[name] = CFuncInfo(
                name,
                scope,
                return_type,
                address,
                return_address,
            )
            return self.dir[name]

    def print(self, verbose: bool) -> None:
        for key, value in self.dir.items():
            if verbose:
                print(f"# Function: {key} with return type: {value.type}")
                print(f"# Resources: {value.resources}")
                print(f"# Start quadruple: {value.start_quad}")
                print(f"# Return address: {value.return_address}")
                print(f"# Parameters list: {[param for param in value.param_list]}")
                print(f"# Address: {value.address}")
            print(value)

class VMFuncDir(Dir[VMFuncInfo]):
    def __init__(self) -> None:
        super().__init__()

    def add(
        self,
        name: str,
        start_quad: int,
        resources: Resources,
    ) -> VMFuncInfo:
        if name in self.dir:
            raise Exception(f"The function {name} is already in the directory.")
        else:
            self.dir[name] = VMFuncInfo(name, start_quad, resources)
            return self.dir[name]

    def print(self, verbose: bool) -> None:
        for key, value in self.dir.items():
            if verbose:
                print(f"# Function: {key}")
                print(f"# Resources: {value.resources}")
                print(f"# Start quadruple: {value.start_quad}")
            else:
                print(value)
