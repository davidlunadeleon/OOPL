from typing import Optional, TypeVar, Generic

from .utils.types import MemoryType, MemoryAddress
from .utils.enums import Types
from .utils.types import Resources
# Generic definition of every accepted var type
T = TypeVar(
    "T", None, bool | None, float | None, int | None, str | None, MemoryAddress | None
)

# Contains a collection of values for a specific type
class MemoryList(Generic[T]):
    values: list[T]
    start_address: int

    def __init__(
        self, start: int, size: Optional[int] = None, default_value: Optional[T] = None
    ) -> None:
        self.start_address = start
        if size is None:
            self.values = []
        else:
            self.values = [default_value for _ in range(size)]


class Memory:
    chunk_size: int
    bools: MemoryList[bool | None]
    floats: MemoryList[float | None]
    ints: MemoryList[int | None]
    strings: MemoryList[str | None]
    ptrs: MemoryList[MemoryAddress | None]

    def __init__(
        self,
        base_address: int,
        chunk_size: int = 1000,
        resources: Optional[Resources] = None,
    ) -> None:
        """
        Basic constructor that either creates memory lists with a defined size for compilation or tailors 
        a new memory list to the specific amount of resources needed during runtime.
        """
        self.chunk_size = chunk_size
        if resources is None:
            self.bools = MemoryList(base_address)
            self.floats = MemoryList(base_address + self.chunk_size)
            self.ints = MemoryList(base_address + self.chunk_size * 2)
            self.strings = MemoryList(base_address + self.chunk_size * 3)
            self.ptrs = MemoryList(base_address + self.chunk_size * 4)
        else:
            self.bools = MemoryList(base_address, resources[0])
            self.floats = MemoryList(base_address + self.chunk_size, resources[1])
            self.ints = MemoryList(base_address + self.chunk_size * 2, resources[2])
            self.strings = MemoryList(base_address + self.chunk_size * 3, resources[3])
            self.ptrs = MemoryList(base_address + self.chunk_size * 4, resources[4])

    def __get_list_from_index(self, index: int) -> MemoryList:
        """
        Get a memory list of a specific type.

        Arguments:
        index: int -- Address that is in the range of a specific memory list.
        """
        if index < self.floats.start_address:
            return self.bools
        elif index < self.ints.start_address:
            return self.floats
        elif index < self.strings.start_address:
            return self.ints
        elif index < self.ptrs.start_address:
            return self.strings
        else:
            return self.ptrs

    def __get_list_from_t(self, t: str) -> MemoryList:
        """
        Get a memory list of a specific type.

        Arguments:
        t: str -- Type wanted.
        """
        match t:
            case Types.BOOL.value:
                return self.bools
            case Types.FLOAT.value:
                return self.floats
            case Types.FLOAT.value:
                return self.floats
            case Types.INT.value:
                return self.ints
            case Types.STRING.value:
                return self.strings
            case Types.PTR.value:
                return self.ptrs
            case _:
                raise TypeError("Can't retrieve a list from invalid type.")

    def __getitem__(self, index: MemoryAddress) -> MemoryType:
        """
        Get the type of an entry of a memory list.

        Arguments:
        index: MemoryAddress -- Address where the entry is stored.
        """
        l = self.__get_list_from_index(index)
        return l.values[index - l.start_address]

    def __setitem__(self, index: int, value: MemoryType) -> None:
        """
        Set the content of an entry on a memory list.

        Arguments:
        index: int -- Address where the entry is.
        value: MemoryType -- Type of the value stored.
        """
        l = self.__get_list_from_index(index)

        match l:
            case self.bools:
                if not isinstance(value, bool):
                    value = True if value == "True" else False
            case self.floats:
                value = float(value)
            case self.ints:
                value = int(value)
            case self.strings:
                value = str(value)
            case self.ptrs:
                self[l.values[index - l.start_address]] = value
                return

        l.values[index - l.start_address] = value

    def __append(self, l: MemoryList, value: MemoryType | None) -> MemoryAddress:
        """
        Insert a new entry on a memory list.

        Arguments:
        l: MemoryList -- List where the entry will be stored.
        value: MemoryType -- Type of the value stored.
        """
        l.values.append(value)
        l_len = len(l.values) - 1
        if l_len > self.chunk_size:
            raise Exception("Chunk size exceeded!")
        else:
            return l_len + l.start_address

    def save_ptr(self, index: int, value: int) -> None:
        """
        Save the instruction pointer our memory.

        Arguments:
        index: int -- Address where the entry should be.
        value: int -- Last quadruple executed.
        """
        l = self.ptrs
        l.values[index - l.start_address] = value

    def append(self, type: str, value: MemoryType) -> MemoryAddress:
        """
        Insert a new value to a memory list from our memory.

        Arguments:
        type:str -- Type of the value to be stored.
        value: MemoryType: Type of the value to be stored.
        """
        l = self.__get_list_from_t(type)
        return self.__append(l, value)

    def reserve(self, t: str, size: int = 1) -> MemoryAddress:
        """
        Reserve a space of memory for future operations corresponding to the correct type.

        Arguments:
        t: str -- Type of variable to be stored.
        size: int = 1 -- Size of the memory space needed, can vary depending on simple vs array variable.
        """
        l = self.__get_list_from_t(t)
        initial_address = self.__append(l, None)
        [self.__append(l, None) for _ in range(size - 1)]
        return initial_address

    def find(self, type: str, value: MemoryType) -> MemoryAddress | None:
        """
        Get address for a specific value type.

        Arguments:
        index: int -- Address where the entry will be stored.
        value: MemoryType -- Type of the value stored.
        """
        l = self.__get_list_from_t(type)
        try:
            return l.values.index(value) + l.start_address
        except ValueError:
            return None

    def clear(self) -> None:
        """
        Delete all content of memory lists.
        """
        self.bools.values.clear()
        self.floats.values.clear()
        self.ints.values.clear()
        self.strings.values.clear()

    def describe_resources(self) -> Resources:
        """
        Get amount of resources needed per type.
        """
        return (
            len(self.bools.values),
            len(self.floats.values),
            len(self.ints.values),
            len(self.strings.values),
            len(self.ptrs.values),
        )

    def is_ptr(self, address: MemoryAddress) -> bool:
        """
        Check if the content of a memory address is a pointer.

        Arguments:
        address: MemoryAddress -- Address where the entry is stored.
        """
        l = self.__get_list_from_index(address)
        return l == self.ptrs

    def print(self, verbose: bool, comment: bool = False):
        """
        Printing to show information about the memory lists depending on verbose value.
        """
        if verbose:
            print("# bools")
        for index, item in enumerate(self.bools.values):
            print(f"{'# ' if comment else ''}{index + self.bools.start_address},{item}")
        if verbose:
            print("# floats")
        for index, item in enumerate(self.floats.values):
            print(
                f"{'# ' if comment else ''}{index + self.floats.start_address},{item}"
            )
        if verbose:
            print("# ints")
        for index, item in enumerate(self.ints.values):
            print(f"{'# ' if comment else ''}{index + self.ints.start_address},{item}")
        if verbose:
            print("# strings")
        for index, item in enumerate(self.strings.values):
            print(
                f"{'# ' if comment else ''}{index + self.strings.start_address},{item}"
            )
        if verbose:
            print("# ptrs")
        for index, item in enumerate(self.ptrs.values):
            print(f"{'# ' if comment else ''}{index + self.ptrs.start_address},{item}")
