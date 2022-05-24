from .utils.types import Quadruple


class QuadrupleList:
    quads: list[Quadruple]
    ptr: int

    def __init__(self) -> None:
        self.ptr = 0
        self.quads = []

    def add(self, quad: Quadruple) -> None:
        self.ptr += 1
        self.quads.append(quad)

    def __getitem__(self, index: int) -> Quadruple:
        return self.quads[index]

    def __setitem__(self, index: int, quad: Quadruple) -> None:
        self.quads[index] = quad

    def print(self, verbose: bool) -> None:
        for index, quad in enumerate(self.quads):
            if verbose:
                print(f"# {index}")
            print(f"{quad[0].value},{quad[1]},{quad[2]},{quad[3]}")

    def reset_ptr(self) -> None:
        self.ptr = 0

    def __iter__(self):
        self.reset_ptr()
        return self

    def __next__(self):
        if self.ptr < len(self.quads):
            self.ptr += 1
            return self.quads[self.ptr - 1]
        else:
            raise StopIteration
