from typing import Optional, TypeVar, Generic

from .utils.types import MemoryType

T = TypeVar("T")


class MemoryList(Generic[T]):
    values: list[T]
    start_address: int

    def __init__(self, start: int) -> None:
        self.start_address = start
        self.values = []


class Memory:
    __default_chunk_size: int
    chunk_size: int
    bools: MemoryList[bool]
    floats: MemoryList[float]
    ints: MemoryList[int]
    strings: MemoryList[str]

    def __init__(self, chunk_size: Optional[int] = None) -> None:
        self.__default_chunk_size = 1000
        if chunk_size is None:
            self.chunk_size = self.__default_chunk_size
        else:
            self.chunk_size = chunk_size
        self.bools = MemoryList(0)
        self.floats = MemoryList(self.chunk_size)
        self.ints = MemoryList(self.chunk_size * 2)
        self.strings = MemoryList(self.chunk_size * 3)

    def __get_list_from_index(self, index: int) -> MemoryList:
        if index < self.floats.start_address:
            return self.bools
        elif index < self.ints.start_address:
            return self.floats
        elif index < self.strings.start_address:
            return self.ints
        else:
            raise TypeError("Can't retrieve a list from an invalid index.")

    def __get_list_from_type(self, value: MemoryType) -> MemoryList:
        if isinstance(value, bool):
            return self.bools
        elif isinstance(value, float):
            return self.floats
        elif isinstance(value, int):
            return self.bools
        elif isinstance(value, str):
            return self.bools
        else:
            raise TypeError("Can't retrieve a list from invalid type.")

    def __getitem__(self, index: int) -> MemoryType:
        return self.__get_list_from_index(index).values[index]

    def __setitem__(self, index: int, value: MemoryType) -> None:
        l = self.__get_list_from_index(index)
        index -= l.start_address
        l.values[index] = value

    def append(self, value: MemoryType) -> int:
        l = self.__get_list_from_type(value)
        l.values.append(value)
        l_len = len(l.values) - 1 + l.start_address
        if l_len > self.chunk_size:
            raise Exception("Chunk size exceeded!")
        else:
            return l_len

    def find(self, value: MemoryType) -> int | None:
        l = self.__get_list_from_type(value)
        try:
            return l.values.index(value)
        except ValueError:
            return None
