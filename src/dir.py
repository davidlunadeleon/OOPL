from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Dir(ABC, Generic[T]):
    dir: dict[str, T]

    def __init__(self):
        self.dir = {}

    @abstractmethod
    def add(self) -> T:
        """
        Insert a new item to the directory.
        """
        pass

    @abstractmethod
    def print(self, verbose: bool) -> None:
        """
        Print the directory.
        """
        pass

    def get(self, name: str) -> T:
        """
        Get an item in the directory.
        """
        if (func_info := self.dir.get(name)) is not None:
            return func_info
        else:
            raise Exception(f"Couldn't retrieve the information of function {name}.")

    def has(self, name: str) -> bool:
        """
        Check whether a function is contained in the directory.
        """
        return False if self.dir.get(name) is None else True

    def values(self) -> list[T]:
        """
        Get all the items in the directory.
        """
        return list(self.dir.values())
