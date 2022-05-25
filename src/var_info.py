from .array_info import ArrayInfo
from .utils.enums import Types
from .utils.types import MemoryAddress


class VarInfo:
    name: str
    type: Types
    address: MemoryAddress
    array_info: ArrayInfo | None

    def __init__(
        self,
        name: str,
        type: Types,
        address: MemoryAddress,
        array_info: ArrayInfo | None,
    ) -> None:
        self.name = name
        self.type = type
        self.address = address
        self.array_info = array_info

    def __str__(self) -> str:
        return f"<name:{self.name},type:{self.type.value},address:{self.address},array_info:{self.array_info}>"