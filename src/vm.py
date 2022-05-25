import sys

from .func_dir import VMFuncDir
from .memory import Memory
from .quadruple_list import QuadrupleList
from .utils.types import FunctionResources, Quadruple, MemoryType, MemoryAddress
from .utils.enums import Operations


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
        self.function_memory = Memory(4000, 1000, (1000, 1000, 1000, 1000))

    def add_function(self, name: str, start_quad: int, resources: FunctionResources):
        self.func_dir.add(name, start_quad, resources)

    def add_quadruple(self, quad: Quadruple):
        self.quads.add(quad)

    def set_global_variable(self, addr: int, val: MemoryType):
        self.global_memory[addr] = val

    def __get_memory(self, address: MemoryAddress):
        return (
            self.function_memory
            if address is not None and address >= 4000
            else self.global_memory
        )

    def run(self):
        quads_iter = iter(self.quads)
        for quad in quads_iter:
            op_code, addr1, addr2, addr3 = quad
            mem1 = self.__get_memory(addr1)
            mem2 = self.__get_memory(addr2)

            if op_code is Operations.GOSUB:
                continue

            if isinstance(addr3, str) or addr3 is None:
                addr3 = 0
            mem3 = self.__get_memory(addr3)

            if op_code is Operations.AND:
                mem3[addr3] = mem1[addr1] and mem2[addr2]
            elif op_code is Operations.ASSIGNOP:
                mem3[addr3] = mem1[addr1]
            elif op_code is Operations.DIFF:
                mem3[addr3] = mem1[addr1] != mem2[addr2]
            elif op_code is Operations.DIVIDES:
                mem3[addr3] = mem1[addr1] / mem2[addr2]
            elif op_code is Operations.ENDSUB:
                pass
            elif op_code is Operations.EQ:
                mem3[addr3] = mem1[addr1] == mem2[addr2]
            elif op_code is Operations.EQGT:
                mem3[addr3] = mem1[addr1] >= mem2[addr2]
            elif op_code is Operations.EQLT:
                mem3[addr3] = mem1[addr1] <= mem2[addr2]
            elif op_code is Operations.GOTOF:
                pass
            elif op_code is Operations.GOTOT:
                pass
            elif op_code is Operations.GT:
                mem3[addr3] = mem1[addr1] > mem2[addr2]
            elif op_code is Operations.LT:
                mem3[addr3] = mem1[addr1] < mem2[addr2]
            elif op_code is Operations.MINUS:
                mem3[addr3] = mem1[addr1] - mem2[addr2]
                pass
            elif op_code is Operations.OR:
                mem3[addr3] = mem1[addr1] or mem2[addr2]
                pass
            elif op_code is Operations.PARAM:
                pass
            elif op_code is Operations.PLUS:
                mem3[addr3] = mem1[addr1] + mem2[addr2]
                pass
            elif op_code is Operations.PRINT:
                print(mem1[addr1])
            elif op_code is Operations.READ:
                mem3[addr3] = sys.stdin.readline()
            elif op_code is Operations.TIMES:
                mem3[addr3] = mem1[addr1] * mem2[addr2]
