from typing import Tuple, TypeAlias

from .enums import Operations

# Parsing and lexing
TokenList = list[str]

# Quadruple handling
MemoryAddress: TypeAlias = int
MemoryType = bool | float | int | str
Quadruple = Tuple[Operations, MemoryAddress, MemoryAddress, MemoryAddress]
TypeAddress = Tuple[str, MemoryAddress, str | None]

NumBools: TypeAlias = int
NumFloats: TypeAlias = int
NumInts: TypeAlias = int
NumStrings: TypeAlias = int
NumPointers: TypeAlias = int
Resources = Tuple[NumBools, NumFloats, NumInts, NumStrings, NumPointers]

ParamName: TypeAlias = str
ParamList: TypeAlias = list[Tuple[str, MemoryAddress, ParamName]]
