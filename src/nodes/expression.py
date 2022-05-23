from ..memory import Memory
from ..quadruple_list import QuadrupleList
from ..scope_stack import ScopeStack
from ..semantic_cube import SemanticCube
from ..utils.enums import Operations, Types
from ..utils.types import TypeAddress, MemoryAddress


class Expression:
    type: Types
    addr: MemoryAddress
    name: str | None

    def __init__(
        self,
        left: TypeAddress,
        op_code: Operations,
        right: TypeAddress,
        mem: Memory,
        quads: QuadrupleList,
        scope_stack: ScopeStack,
    ) -> None:
        l_type, l_addr, l_name = left
        r_type, r_addr, _ = right
        self.type = SemanticCube().get(l_type, op_code, r_type)
        if op_code is Operations.ASSIGNOP:
            if l_name is not None and scope_stack.has_var(l_name):
                quads.add((op_code, r_addr, None, l_addr))
                self.addr = l_addr
                self.name = l_name
            else:
                raise Exception(f"Only variables may be assigned to.")
        else:
            self.addr = mem.reserve(self.type)
            self.name = None
            quads.add((op_code, l_addr, r_addr, self.addr))

    def get(self) -> TypeAddress:
        return (self.type, self.addr, self.name)
