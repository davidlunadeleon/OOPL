from ..memory import Memory, MemoryType
from ..utils.enums import Types
from ..utils.types import MemoryAddress, TypeAddress


class Constant:
    val: MemoryType
    type: Types
    address: MemoryAddress

    def __init__(self, const_val: str, const_type: Types, memory: Memory) -> None:
        self.type = const_type
        match self.type:
            case Types.BOOL:
                self.val = True if const_val == "True" else False
            case Types.FLOAT:
                self.val = float(const_val)
            case Types.INT:
                self.val = int(const_val)
            case Types.STRING:
                self.val = str(const_val).removeprefix('"').removesuffix('"')
            case _:
                raise TypeError("Invalid type passed to Constant constructor.")
        if (address := memory.find(self.type, self.val)) is not None:
            self.address = address
        else:
            self.address = memory.append(self.type, self.val)

    def get(self) -> TypeAddress:
        return (self.type, self.address, None)
