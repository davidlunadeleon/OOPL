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
        self.ptr += 1
        self.quads.append(quad)

    def __getitem__(self, address: MemoryAddress) -> Quadruple:
        index = int(self.mem[address])
        return self.quads[index]

    def __setitem__(self, address: MemoryAddress, quad: Quadruple) -> None:
        index = int(self.mem[address])
        self.quads[index] = quad

    def print(self, verbose: bool) -> None:
        if verbose:
            for index, quad in enumerate(self.quads):
                print(f"# {index}\t{quad[0].value},{quad[1]},{quad[2]},{quad[3]}")
        for index, quad in enumerate(self.quads):
            print(f"{quad[0].value},{quad[1]},{quad[2]},{quad[3]}")

    def reset_ptr(self) -> None:
        self.ptr = 0

    def ptr_address(self, offset: int = 0) -> MemoryAddress:
        _, address, _ = Constant(str(self.ptr + offset), Types.INT, self.mem).get()
        return address

    def __iter__(self):
        self.reset_ptr()
        return self

    def __next__(self):
        if self.ptr < len(self.quads):
            self.ptr += 1
            return self.quads[self.ptr - 1]
        else:
            raise StopIteration
