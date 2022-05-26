from typing import Tuple, TypeAlias

from .enums import Operations, Types

# Parsing and lexing
TokenList = list[str]

# Quadruple handling
MemoryAddress: TypeAlias = int
MemoryType = bool | float | int | str
Quadruple = Tuple[
    Operations, MemoryAddress | None, MemoryAddress | None, MemoryAddress | str | None
]
FunctionResources = Tuple[int, int, int, int]
TypeAddress = Tuple[Types, MemoryAddress, str | None]

ParamName: TypeAlias = str
ParamList: TypeAlias = list[Tuple[Types, MemoryAddress, ParamName]]
