from typing import Tuple
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
        self.function_memory = Memory(5000, 1000, (0, 0, 0, 0, 0))
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
            if address is not None and address >= 5000
            else self.global_memory
        )

    def __reserve_memory(self, func_address: MemoryAddress) -> None:
        self.temp_memory = Memory(
            5000,
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

            match quad:
                case (Operations.PRINT, int(addr1), None, None):
                    if op_code is Operations.PRINT:
                        print(mem1[addr1], end="")
                    else:
                        raise Exception("Cannot print from a None memory address.")
                case (Operations.GOSUB, None, None, int(addr3)):
                    self.__save_state(addr3, mem1)
                case (Operations.ERA, None, None, int(addr3)):
                    self.__reserve_memory(addr3)
                case (Operations.GOTO, None, None, int(addr3)):
                    self.quads.ptr = int(mem3[addr3])
                case (Operations.READ, None, None, int(addr3)):
                    mem3[addr3] = sys.stdin.readline()
                case (Operations.GOTOF, int(addr1), None, int(addr3)):
                    if not mem1[addr1]:
                        self.quads.ptr = int(mem3[addr3])
                case (Operations.GOTOT, int(addr1), None, int(addr3)):
                    if mem1[addr1]:
                        self.quads.ptr = int(mem3[addr3])
                case (Operations.ASSIGNOP, int(addr1), None, int(addr3)):
                    mem3[addr3] = mem1[addr1]
                case (Operations.PARAM, int(addr1), None, int(addr3)):
                    self.temp_memory[addr3] = mem1[addr1]
                case (Operations.SAVEPTR, int(addr1), None, int(addr3)):
                    mem3.save_ptr(addr3, mem1[addr1])
                case (Operations.AND, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] and mem2[addr2]
                case (Operations.DIFF, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] != mem2[addr2]
                case (Operations.DIVIDES, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] / mem2[addr2]
                case (Operations.EQ, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] == mem2[addr2]
                case (Operations.EQGT, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] >= mem2[addr2]
                case (Operations.EQLT, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] <= mem2[addr2]
                case (Operations.GT, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] > mem2[addr2]
                case (Operations.LT, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] < mem2[addr2]
                case (Operations.MINUS, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] - mem2[addr2]
                case (Operations.OR, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] or mem2[addr2]
                case (Operations.PLUS, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] + mem2[addr2]
                case (Operations.TIMES, int(addr1), int(addr2), int(addr3)):
                    mem3[addr3] = mem1[addr1] * mem2[addr2]
                case (Operations.VER, int(addr1), int(addr2), int(addr3)):
                    if not (mem2[addr2] <= mem1[addr1] and mem1[addr1] < mem3[addr3]):
                        raise Exception("Out of bounds error.")
                case (Operations.ENDSUB, None, None, None):
                    if op_code is Operations.ENDSUB:
                        if self.__restore_state():
                            return
