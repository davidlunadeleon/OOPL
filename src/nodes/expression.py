from ..memory import Memory
from ..quadruple_list import QuadrupleList
from ..semantic_cube import SemanticCube
from ..utils.enums import Operations, Types
from ..utils.types import TypeAddress, MemoryAddress


class Expression:
    type: Types
    addr: MemoryAddress

    def __init__(
        self,
        left: TypeAddress,
        op_code: Operations,
        right: TypeAddress,
        mem: Memory,
        quads: QuadrupleList,
    ) -> None:
        l_type, l_addr = left
        r_type, r_addr = right
        self.type = SemanticCube().get(l_type, op_code, r_type)
        if op_code is Operations.ASSIGNOP:
            quads.add((op_code, r_addr, None, l_addr))
            self.addr = l_addr
        else:
            self.addr = mem.reserve(self.type)
            quads.add((op_code, l_addr, r_addr, self.addr))

    def get(self) -> TypeAddress:
        return (self.type, self.addr)
