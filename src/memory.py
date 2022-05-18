from typing import Optional, TypeVar, Generic

from .utils.types import MemoryType, MemoryAddress
from .utils.enums import Types
from .utils.types import FunctionResources

T = TypeVar("T")


class MemoryList(Generic[T]):
    values: list[T]
    start_address: int

    def __init__(self, start: int) -> None:
        self.start_address = start
        self.values = []


class Memory:
    chunk_size: int
    bools: MemoryList[bool | None]
    floats: MemoryList[float | None]
    ints: MemoryList[int | None]
    strings: MemoryList[str | None]

    def __init__(self, base_address: int, chunk_size: int = 1000) -> None:
        self.chunk_size = chunk_size
        self.bools = MemoryList(base_address)
        self.floats = MemoryList(base_address + self.chunk_size)
        self.ints = MemoryList(base_address + self.chunk_size * 2)
        self.strings = MemoryList(base_address + self.chunk_size * 3)

    def __get_list_from_index(self, index: int) -> MemoryList:
        if index < self.floats.start_address:
            return self.bools
        elif index < self.ints.start_address:
            return self.floats
        elif index < self.strings.start_address:
            return self.ints
        else:
            return self.strings

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

    def __getitem__(self, index: MemoryAddress) -> MemoryType:
        if isinstance(index, int):
            l = self.__get_list_from_index(index)
            return l.values[index - l.start_address]
        else:
            raise Exception("Can't access an invalid memory address.")

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

    def clear(self) -> None:
        self.bools.values.clear()
        self.floats.values.clear()
        self.ints.values.clear()
        self.strings.values.clear()

    def describe_resources(self) -> FunctionResources:
        return (
            len(self.bools.values),
            len(self.floats.values),
            len(self.ints.values),
            len(self.strings.values),
        )

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
