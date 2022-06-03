from typing import Tuple
import sys

from .func_dir import VMFuncDir
from .memory import Memory
from .quadruple_list import QuadrupleList
from .utils.types import Resources, Quadruple, MemoryType, MemoryAddress
from .utils.enums import Operations
from .utils.errors import VMError, OOPLErrorTypes

start_global_memory = 1
start_function_memory = 5001
chunk_size = 1000


class VM:
    function_memory: Memory
    func_dir: VMFuncDir
    global_memory: Memory
    temp_memory: Memory
    memory_stack: list[Tuple[Memory, int]]
    quads: QuadrupleList
    last_return: MemoryType

    def __init__(self) -> None:
        self.func_dir = VMFuncDir()
        self.memory_stack = []

    def init_global_memory(self, global_resources: Resources) -> None:
        """
        Starting a global memory that will be accessible to all contexts.
        """
        self.global_memory = Memory(start_global_memory, chunk_size, global_resources)
        self.function_memory = Memory(
            start_function_memory, chunk_size, (0, 0, 0, 0, 0)
        )
        self.quads = QuadrupleList(self.global_memory)

    def add_function(self, name: str, start_quad: int, resources: Resources):
        """
        Inserting a new function to directory.

        Arguments:
        name: str -- Name of the function.
        start_quad: int -- Number of the quadruple where the function starts.
        resources: Resources -- The information about the amount of resources of each type needed for the function.
        """
        self.func_dir.add(name, start_quad, resources)

    def add_quadruple(self, quad: Quadruple):
        """
        Insert a new quadruple to list.

        Arguments:
        quad: Quarduple -- The quadruple to be inserted.
        """
        self.quads.add(quad)

    def set_global_variable(self, addr: int, val: MemoryType):
        """
        Setting a global variable according to a known address.

        Arguments:
        addr: int -- The space in the global memory where the variable should be stored.
        val: MemoryType: The type of the variable asigned.
        """
        self.global_memory[addr] = val

    def __get_memory(self, address: MemoryAddress | None):
        """
        Get either the global or function memory depending in which range the address is in.

        Arguments:
        address: MemoryAddress -- Address targeted.
        """
        return (
            self.function_memory
            if address is not None and address >= start_function_memory
            else self.global_memory
        )

    def __reserve_memory(self, func_address: MemoryAddress) -> None:
        """ "
        Reserve the memory for the function that is being called.

        Arguments:
        func_address: MemoryAddress -- Address where the function name is stored.
        """
        self.temp_memory = Memory(
            start_function_memory,
            chunk_size,
            self.func_dir.get(str(self.global_memory[func_address])).resources,
        )

    def __restore_state(self) -> bool:
        """
        Delete the temporary function memory that was being executed and reawaken the previous function memory.
        If there is no other one, then notify to use global memory.
        """
        self.temp_memory.clear()
        self.function_memory, self.quads.ptr = self.memory_stack.pop()
        if len(self.memory_stack) == 0:
            return True
        else:
            return False

    def __save_state(self, func_address: MemoryAddress, mem: Memory) -> None:
        """
        Store the previous function memory being used to change context to the new one. Also, go towards the
        quadruples that correspond to the new one.
        """
        self.memory_stack.append((self.function_memory, self.quads.ptr))
        self.function_memory = self.temp_memory
        self.quads.ptr = int(
            mem[self.func_dir.get(str(self.global_memory[func_address])).start_quad]
        )

    def __check_none(self, l: list[Tuple[MemoryType, MemoryAddress]]) -> None:
        for val, addr in l:
            if val is None:
                raise VMError(
                    OOPLErrorTypes.UNINITIALIZED_VARIABLE,
                    f"the variable at address {addr} is uninitialized",
                )

    def run(self) -> MemoryType:
        """
        Carry out the operations described on the quadruples and also solve the expressions.
        """
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
            # When using arrays, the last element of a quadruple could be a pointer, so we need to check to obtain its content
            if addr3 != 0 and mem3.is_ptr(addr3) and op_code is not Operations.SAVEPTR:
                temp_mem = self.__get_memory(int(mem3[addr3]))
                addr3 = int(mem3[addr3])
                mem3 = temp_mem

            # print((op_code, addr1, addr2, addr3))

            match op_code:
                case Operations.PRINT:
                    self.__check_none([(mem1[addr1], addr1)])
                    print(mem1[addr1], end="")
                case Operations.GOSUB:
                    self.__save_state(addr3, mem1)
                case Operations.ERA:
                    self.__reserve_memory(addr3)
                case Operations.GOTO:
                    self.__check_none([(mem3[addr3], addr3)])
                    self.quads.ptr = int(mem3[addr3])
                case Operations.READ:
                    mem3[addr3] = input()
                case Operations.GOTOF:
                    self.__check_none([(mem1[addr1], addr1), (mem3[addr3], addr3)])
                    if not mem1[addr1]:
                        self.quads.ptr = int(mem3[addr3])
                case Operations.GOTOT:
                    self.__check_none([(mem1[addr1], addr1), (mem3[addr3], addr3)])
                    if mem1[addr1]:
                        self.quads.ptr = int(mem3[addr3])
                case Operations.ASSIGNOP:
                    self.__check_none([(mem1[addr1], addr1)])
                    self.last_return = mem1[addr1]
                    mem3[addr3] = mem1[addr1]
                case Operations.PARAM:
                    # Need to use temporary memory to pass value from one context to another
                    # (previous function to new one)
                    self.__check_none([(mem1[addr1], addr1)])
                    self.temp_memory[addr3] = mem1[addr1]
                case Operations.OPT_ASSIGN:
                    if mem1[addr1] is not None:
                        mem3[addr3] = mem1[addr1]
                case Operations.OPT_PARAM:
                    if mem1[addr1] is not None:
                        self.temp_memory[addr3] = mem1[addr1]
                case Operations.SAVEPTR:
                    self.__check_none([(mem1[addr1], addr1)])
                    mem3.save_ptr(addr3, mem1[addr1])
                case Operations.AND:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] and mem2[addr2]
                case Operations.DIFF:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] != mem2[addr2]
                case Operations.DIVIDES:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] / mem2[addr2]
                case Operations.EQ:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] == mem2[addr2]
                case Operations.EQGT:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] >= mem2[addr2]
                case Operations.EQLT:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] <= mem2[addr2]
                case Operations.GT:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] > mem2[addr2]
                case Operations.LT:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] < mem2[addr2]
                case Operations.MINUS:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] - mem2[addr2]
                case Operations.OR:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] or mem2[addr2]
                case Operations.PLUS:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] + mem2[addr2]
                case Operations.TIMES:
                    self.__check_none([(mem1[addr1], addr1), (mem2[addr2], addr2)])
                    mem3[addr3] = mem1[addr1] * mem2[addr2]
                # Check that the value is not out of bounds of the dimension
                case Operations.VER:
                    self.__check_none(
                        [
                            (mem1[addr1], addr1),
                            (mem2[addr2], addr2),
                            (mem3[addr3], addr3),
                        ]
                    )
                    if not (mem2[addr2] <= mem1[addr1] and mem1[addr1] < mem3[addr3]):
                        raise Exception("Out of bounds error.")
                case Operations.ENDSUB:
                    if op_code is Operations.ENDSUB:
                        if self.__restore_state():
                            return self.last_return
                case _:
                    raise VMError(
                        OOPLErrorTypes.UNKNOWN_QUADRUPLE,
                        f"cannot handle unknown quadruple {quad}",
                    )
        raise VMError(
            OOPLErrorTypes.EMPTY_QUADRUPLES, "cannot run on an empty quadruple list"
        )
