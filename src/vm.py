from .quadruple_list import QuadrupleList
from .utils.types import FunctionResources, Quadruple, MemoryType
from .memory import Memory


class VM:
    function_memory: Memory
    global_memory: Memory
    memory_stack: list[Memory]
    quads: QuadrupleList

    def __init__(self) -> None:
        self.global_memory = Memory(0)
        self.quads = QuadrupleList()

    def add_function(self, name: str, resources: FunctionResources, start_quad: int):
        pass

    def add_quadruple(self, quad: Quadruple):
        self.quads.add(quad)

    def add_global_variable(self, addr: int, val: MemoryType):
        self.global_memory[addr] = val

    def run(self):
        quads_iter = iter(self.quads)
        for quad in quads_iter:
            print(quad)
