from typing import Tuple
from copy import copy
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
    temp_memory: Memory
    memory_stack: list[Tuple[Memory, int]]
    quads: QuadrupleList

    def __init__(self) -> None:
        self.func_dir = VMFuncDir()
        self.memory_stack = []

    def init_global_memory(self, global_resources: FunctionResources) -> None:
        self.global_memory = Memory(0, 1000, global_resources)
        self.function_memory = Memory(4000, 1000, (0, 0, 0, 0))
        self.quads = QuadrupleList(self.global_memory)

    def add_function(self, name: str, start_quad: int, resources: FunctionResources):
        self.func_dir.add(name, start_quad, resources)

    def add_quadruple(self, quad: Quadruple):
        self.quads.add(quad)

    def set_global_variable(self, addr: int, val: MemoryType):
        self.global_memory[addr] = val

    def __get_memory(self, address: MemoryAddress | None):
        return (
            self.function_memory
            if address is not None and address >= 4000
            else self.global_memory
        )

    def run(self):
        for quad in self.quads:
            op_code, addr1, addr2, addr3 = quad
            mem1 = self.__get_memory(addr1)
            mem2 = self.__get_memory(addr2)

            if op_code is Operations.GOSUB:
                self.memory_stack.append((copy(self.function_memory), self.quads.ptr))
                self.function_memory = self.temp_memory
                self.quads.ptr = mem1[self.func_dir.get(addr3).start_quad]
            elif op_code is Operations.ERA:
                self.temp_memory = Memory(
                    4000, 1000, self.func_dir.get(addr3).resources
                )

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
                self.temp_memory.clear()
                self.function_memory, self.quads.ptr = self.memory_stack.pop()
                if len(self.memory_stack) == 0:
                    return
            elif op_code is Operations.EQ:
                mem3[addr3] = mem1[addr1] == mem2[addr2]
            elif op_code is Operations.EQGT:
                mem3[addr3] = mem1[addr1] >= mem2[addr2]
            elif op_code is Operations.EQLT:
                mem3[addr3] = mem1[addr1] <= mem2[addr2]
            elif op_code is Operations.GOTO:
                self.quads.ptr = mem3[addr3]
            elif op_code is Operations.GOTOF:
                if not mem1[addr1]:
                    self.quads.ptr = mem3[addr3]
            elif op_code is Operations.GOTOT:
                if mem1[addr1]:
                    self.quads.ptr = mem3[addr3]
            elif op_code is Operations.GT:
                mem3[addr3] = mem1[addr1] > mem2[addr2]
            elif op_code is Operations.LT:
                mem3[addr3] = mem1[addr1] < mem2[addr2]
            elif op_code is Operations.MINUS:
                mem3[addr3] = mem1[addr1] - mem2[addr2]
            elif op_code is Operations.OR:
                mem3[addr3] = mem1[addr1] or mem2[addr2]
            elif op_code is Operations.PARAM:
                self.temp_memory[addr3] = mem1[addr1]
            elif op_code is Operations.PLUS:
                mem3[addr3] = mem1[addr1] + mem2[addr2]
            elif op_code is Operations.PRINT:
                print(mem1[addr1])
            elif op_code is Operations.READ:
                mem3[addr3] = sys.stdin.readline()
            elif op_code is Operations.TIMES:
                mem3[addr3] = mem1[addr1] * mem2[addr2]
