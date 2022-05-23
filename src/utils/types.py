from typing import Tuple

from .enums import Operations, Types

# Parsing and lexing
TokenList = list[str]

# Quadruple handling
MemoryAddress = int | str | None
MemoryType = bool | float | int | str
Quadruple = Tuple[Operations, MemoryAddress | str, MemoryAddress, MemoryAddress]
FunctionResources = Tuple[int, int, int, int]
TypeAddress = Tuple[Types, MemoryAddress, str | None]
