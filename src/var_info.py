from typing import Optional

from .array_info import ArrayInfo
from .utils.types import MemoryAddress


class VarInfo:
    name: str
    type: str
    address: MemoryAddress
    array_info: ArrayInfo | None

    def __init__(
        self,
        name: str,
        type: str,
        address: MemoryAddress = 0,
        array_info: Optional[ArrayInfo] = None,
    ) -> None:
        self.name = name
        self.type = type
        self.address = address
        self.array_info = array_info

    def __str__(self) -> str:
        """
        Stringify the values of VarInfo for readability.
        """
        return f"<name:{self.name},type:{self.type},address:{self.address},array_info:{self.array_info}>"
