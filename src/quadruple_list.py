from .utils.types import Quadruple


class QuadrupleList:
    quads: list[Quadruple]
    ptr: int

    def __init__(self) -> None:
        self.ptr = 0
        self.quads = []

    def add(self, quad: Quadruple) -> None:
        self.quads.append(quad)

    def get(self, index: int) -> Quadruple:
        return self.quads[index]

    def fill(self, index: int, quad: Quadruple) -> None:
        # Offset because array starts at 0 but instructions are counted from 1
        self.quads[index - 1] = quad

    def print(self) -> None:
        # for quad in self.quads:
        #     print(quad)
        for i, quad in enumerate(self.quads):
            print(i + 1, quad)
