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
        self.quads[index] = quad
