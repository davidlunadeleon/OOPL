from ..memory import Memory, MemoryType
from ..utils.enums import Types
from ..utils.types import MemoryAddress, TypeAddress


class Constant:
    val: MemoryType
    type: str
    address: MemoryAddress

    def __init__(self, const_val: str, const_type: str, memory: Memory) -> None:
        self.type = const_type
        match self.type:
            case Types.BOOL.value:
                self.val = True if const_val == "True" else False
            case Types.FLOAT.value:
                self.val = float(const_val)
            case Types.INT.value:
                self.val = int(const_val)
            case Types.STRING.value:
                self.val = str(const_val).removeprefix('"').removesuffix('"')
            case Types.PTR.value:
                self.val = int(const_val)
            case _:
                raise TypeError("Invalid type passed to Constant constructor.")
        if (address := memory.find(self.type, self.val)) is not None:
            self.address = address
        else:
            self.address = memory.append(self.type, self.val)

    def get(self) -> TypeAddress:
        return (self.type, self.address, None)
