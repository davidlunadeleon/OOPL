from typing import Tuple

from .enums import Operations

# Parsing and lexing
TokenList = list[str]

# Quadruple handling
MemoryAddress = int | str | None
MemoryType = bool | float | int | str
Quadruple = Tuple[Operations, MemoryAddress, MemoryAddress, MemoryAddress]
FunctionResources = Tuple[int, int, int, int] | None
