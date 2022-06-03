from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    stack: list[T]

    def __init__(self) -> None:
        self.stack = []

    def push(self, item: T) -> None:
        """
        Insert a new item to the stack.
        """
        self.stack.append(item)

    def pop(self) -> T:
        """
        Pop the last item of the stack.
        """
        return self.stack.pop()

    def top(self) -> T:
        """
        Get the top item to the stack.
        """
        return self.stack[-1]
