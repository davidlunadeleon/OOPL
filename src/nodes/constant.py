from ..memory import Memory, MemoryType
from ..utils.enums import Types
from ..utils.types import MemoryAddress, TypeAddress


class Constant:
    val: MemoryType
    type: Types
    address: MemoryAddress

    def __init__(self, const_val: str, const_type: Types, memory: Memory) -> None:
        self.type = const_type
        if self.type is Types.BOOL:
            self.val = True if const_val == "True" else False
        elif self.type is Types.FLOAT:
            self.val = float(const_val)
        elif self.type is Types.INT:
            self.val = int(const_val)
        elif self.type is Types.STRING:
            self.val = const_val
        else:
            raise TypeError("Invalid type passed to Constant constructor.")
        self.address = memory.append(self.val)

    def get(self) -> TypeAddress:
        return (self.type, self.address)
