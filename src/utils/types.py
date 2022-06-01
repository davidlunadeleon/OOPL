from typing import Tuple, TypeAlias

from .enums import Operations

# Parsing and lexing
TokenList = list[str]

# Quadruple handling
MemoryAddress: TypeAlias = int
MemoryType = bool | float | int | str
Quadruple = Tuple[Operations, MemoryAddress, MemoryAddress, MemoryAddress]
FunctionResources = Tuple[int, int, int, int, int]
TypeAddress = Tuple[str, MemoryAddress, str | None]

ParamName: TypeAlias = str
ParamList: TypeAlias = list[Tuple[str, MemoryAddress, ParamName]]
