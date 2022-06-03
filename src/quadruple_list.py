from .utils.types import Quadruple, MemoryAddress
from .memory import Memory
from .nodes.constant import Constant
from .utils.enums import Types


class QuadrupleList:
    mem: Memory
    quads: list[Quadruple]
    ptr: int

    def __init__(self, mem: Memory) -> None:
        self.mem = mem
        self.ptr = 0
        self.quads = []

    def add(self, quad: Quadruple) -> None:
        """
        Insert a new quadruple to the list and update instruction pointer.

        Arguments:
        quad: Quadruple -- The instruction to be appended.
        """
        self.ptr += 1
        self.quads.append(quad)

    def __getitem__(self, address: MemoryAddress) -> Quadruple:
        """
        Get a quadruple from a specific address.

        Arguments:
        address: MemoryAddress -- The address where the number of the instruction is stored.
        """
        index = int(self.mem[address])
        return self.quads[index]

    def __setitem__(self, address: MemoryAddress, quad: Quadruple) -> None:
        """
        Set a quadruple stored in a specific address.

        Arguments:
        address: MemoryAddress -- Address where the number of the instruction is stored.
        quad: Quadruple -- The quadruple to be assigned.
        """
        index = int(self.mem[address])
        self.quads[index] = quad

    def print(self, verbose: bool) -> None:
        """
        Print the values all the quadruples depending on the value of verbose.
        """
        if verbose:
            for index, quad in enumerate(self.quads):
                print(f"# {index}\t{quad[0].value},{quad[1]},{quad[2]},{quad[3]}")
        for index, quad in enumerate(self.quads):
            print(f"{quad[0].value},{quad[1]},{quad[2]},{quad[3]}")

    def reset_ptr(self) -> None:
        """
        Restarting the instruction pointer to 0.
        """
        self.ptr = 0

    def ptr_address(self, offset: int = 0) -> MemoryAddress:
        """
        Get the address where the instruction pointer is stored.
        """
        _, address, _ = Constant(
            str(self.ptr + offset), Types.INT.value, self.mem
        ).get()
        return address

    def __iter__(self):
        """
        Get an iterator for QuadrupleList and reset instruction pointer.
        """
        self.reset_ptr()
        return self

    def __next__(self):
        """
        Access the next element available for the iterator of QuadrupleList and update instruction pointer accordingly.
        """
        if self.ptr < len(self.quads):
            self.ptr += 1
            return self.quads[self.ptr - 1]
        else:
            raise StopIteration
