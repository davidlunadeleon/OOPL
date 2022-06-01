from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    stack: list[T]

    def __init__(self) -> None:
        self.stack = []

    def push(self, item: T) -> None:
        self.stack.append(item)

    def pop(self) -> T:
        return self.stack.pop()

    def top(self) -> T:
        return self.stack[-1]
