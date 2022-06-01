from typing import Tuple
import sys

from .func_dir import VMFuncDir
from .memory import Memory
from .quadruple_list import QuadrupleList
from .utils.types import Resources, Quadruple, MemoryType, MemoryAddress
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

    def init_global_memory(self, global_resources: Resources) -> None:
        self.global_memory = Memory(1, 1000, global_resources)
        self.function_memory = Memory(5001, 1000, (0, 0, 0, 0, 0))
        self.quads = QuadrupleList(self.global_memory)

    def add_function(self, name: str, start_quad: int, resources: Resources):
        self.func_dir.add(name, start_quad, resources)

    def add_quadruple(self, quad: Quadruple):
        self.quads.add(quad)

    def set_global_variable(self, addr: int, val: MemoryType):
        self.global_memory[addr] = val

    def __get_memory(self, address: MemoryAddress | None):
        return (
            self.function_memory
            if address is not None and address >= 5001
            else self.global_memory
        )

    def __reserve_memory(self, func_address: MemoryAddress) -> None:
        self.temp_memory = Memory(
            5001,
            1000,
            self.func_dir.get(str(self.global_memory[func_address])).resources,
        )

    def __restore_state(self) -> bool:
        self.temp_memory.clear()
        self.function_memory, self.quads.ptr = self.memory_stack.pop()
        if len(self.memory_stack) == 0:
            return True
        else:
            return False

    def __save_state(self, func_address: MemoryAddress, mem: Memory) -> None:
        self.memory_stack.append((self.function_memory, self.quads.ptr))
        self.function_memory = self.temp_memory
        self.quads.ptr = int(
            mem[self.func_dir.get(str(self.global_memory[func_address])).start_quad]
        )

    def run(self):
        for quad in self.quads:
            op_code, addr1, addr2, addr3 = quad
            mem1 = self.__get_memory(addr1)
            mem2 = self.__get_memory(addr2)
            mem3 = self.__get_memory(addr3)

            if addr1 != 0 and mem1.is_ptr(addr1):
                temp_mem = self.__get_memory(int(mem1[addr1]))
                addr1 = int(mem1[addr1])
                mem1 = temp_mem
            if addr2 != 0 and mem2.is_ptr(addr2):
                temp_mem = self.__get_memory(int(mem2[addr2]))
                addr2 = int(mem2[addr2])
                mem2 = temp_mem
            if addr3 != 0 and mem3.is_ptr(addr3) and op_code is not Operations.SAVEPTR:
                temp_mem = self.__get_memory(int(mem3[addr3]))
                addr3 = int(mem3[addr3])
                mem3 = temp_mem

            match op_code:
                case Operations.PRINT:
                    print(mem1[addr1], end="")
                case Operations.GOSUB:
                    self.__save_state(addr3, mem1)
                case Operations.ERA:
                    self.__reserve_memory(addr3)
                case Operations.GOTO:
                    self.quads.ptr = int(mem3[addr3])
                case Operations.READ:
                    mem3[addr3] = input()
                case Operations.GOTOF:
                    if not mem1[addr1]:
                        self.quads.ptr = int(mem3[addr3])
                case Operations.GOTOT:
                    if mem1[addr1]:
                        self.quads.ptr = int(mem3[addr3])
                case Operations.ASSIGNOP:
                    mem3[addr3] = mem1[addr1]
                case Operations.PARAM:
                    self.temp_memory[addr3] = mem1[addr1]
                case Operations.SAVEPTR:
                    mem3.save_ptr(addr3, mem1[addr1])
                case Operations.AND:
                    mem3[addr3] = mem1[addr1] and mem2[addr2]
                case Operations.DIFF:
                    mem3[addr3] = mem1[addr1] != mem2[addr2]
                case Operations.DIVIDES:
                    mem3[addr3] = mem1[addr1] / mem2[addr2]
                case Operations.EQ:
                    mem3[addr3] = mem1[addr1] == mem2[addr2]
                case Operations.EQGT:
                    mem3[addr3] = mem1[addr1] >= mem2[addr2]
                case Operations.EQLT:
                    mem3[addr3] = mem1[addr1] <= mem2[addr2]
                case Operations.GT:
                    mem3[addr3] = mem1[addr1] > mem2[addr2]
                case Operations.LT:
                    mem3[addr3] = mem1[addr1] < mem2[addr2]
                case Operations.MINUS:
                    mem3[addr3] = mem1[addr1] - mem2[addr2]
                case Operations.OR:
                    mem3[addr3] = mem1[addr1] or mem2[addr2]
                case Operations.PLUS:
                    mem3[addr3] = mem1[addr1] + mem2[addr2]
                case Operations.TIMES:
                    mem3[addr3] = mem1[addr1] * mem2[addr2]
                case Operations.VER:
                    if not (mem2[addr2] <= mem1[addr1] and mem1[addr1] < mem3[addr3]):
                        raise Exception("Out of bounds error.")
                case Operations.ENDSUB:
                    if op_code is Operations.ENDSUB:
                        if self.__restore_state():
                            return
