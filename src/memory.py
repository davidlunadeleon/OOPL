from typing import Optional, TypeVar, Generic

from .utils.types import MemoryType, MemoryAddress
from .utils.enums import Types

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
    bools: MemoryList[bool | None]
    floats: MemoryList[float | None]
    ints: MemoryList[int | None]
    strings: MemoryList[str | None]

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
            return self.ints
        elif isinstance(value, str):
            return self.strings
        else:
            raise TypeError("Can't retrieve a list from invalid type.")

    def __get_list_from_t(self, t: Types) -> MemoryList:
        if t == Types.BOOL:
            return self.bools
        elif t == Types.FLOAT:
            return self.floats
        elif t == Types.INT:
            return self.ints
        elif t == Types.STRING:
            return self.strings
        else:
            raise TypeError("Can't retrieve a list from invalid type.")

    def __getitem__(self, index: int) -> MemoryType:
        return self.__get_list_from_index(index).values[index]

    def __setitem__(self, index: int, value: MemoryType) -> None:
        l = self.__get_list_from_index(index)
        index -= l.start_address
        l.values[index] = value

    def __append(self, l: MemoryList, value: MemoryType | None) -> MemoryAddress:
        l.values.append(value)
        l_len = len(l.values) - 1
        if l_len > self.chunk_size:
            raise Exception("Chunk size exceeded!")
        else:
            return l_len + l.start_address

    def append(self, value: MemoryType) -> MemoryAddress:
        l = self.__get_list_from_type(value)
        return self.__append(l, value)

    def reserve(self, t: Types) -> MemoryAddress:
        l = self.__get_list_from_t(t)
        return self.__append(l, None)

    def find(self, value: MemoryType) -> MemoryAddress:
        l = self.__get_list_from_type(value)
        try:
            return l.values.index(value) + l.start_address
        except ValueError:
            return None

    def print(self):
        print("bools")
        for index, item in enumerate(self.bools.values):
            print(f"{index + self.bools.start_address}\t{item}")
        print("floats")
        for index, item in enumerate(self.floats.values):
            print(f"{index + self.floats.start_address}\t{item}")
        print("ints")
        for index, item in enumerate(self.ints.values):
            print(f"{index + self.ints.start_address}\t{item}")
        print("strings")
        for index, item in enumerate(self.strings.values):
            print(f"{index + self.strings.start_address}\t{item}")
