from .func_dir import VMFuncDir
from .memory import Memory
from .quadruple_list import QuadrupleList
from .utils.types import FunctionResources, Quadruple, MemoryType


class VM:
    function_memory: Memory
    func_dir: VMFuncDir
    global_memory: Memory
    memory_stack: list[Memory]
    quads: QuadrupleList

    def __init__(self) -> None:
        self.quads = QuadrupleList()
        self.func_dir = VMFuncDir()

    def init_global_memory(self, global_resources: FunctionResources) -> None:
        self.global_memory = Memory(0, 1000, global_resources)

    def add_function(self, name: str, start_quad: int, resources: FunctionResources):
        self.func_dir.add(name, start_quad, resources)

    def add_quadruple(self, quad: Quadruple):
        self.quads.add(quad)

    def set_global_variable(self, addr: int, val: MemoryType):
        self.global_memory[addr] = val

    def run(self):
        quads_iter = iter(self.quads)
        for quad in quads_iter:
            print(quad)
