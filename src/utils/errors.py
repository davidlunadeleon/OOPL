from enum import Enum
from typing import TypeAlias


class OOPLErrorTypes(Enum):
    DUPLICATE = "duplicate entity"
    IMPLICIT_DECLARATION = "implicit function declaration"
    NULL_DEREF = "null pointer dereference"
    SEMANTIC = "semantic"
    SYNTAX = "syntax"
    TYPE_MISMATCH = "type mismatch"
    UNDECLARED_IDENTIFIER = "undeclared identifier"


class OOPLError(Exception):
    message: str
    type: OOPLErrorTypes

    def __init__(self, type: OOPLErrorTypes, message: str) -> None:
        super().__init__(message)
        self.type = type

    def __str__(self) -> str:
        return f"{self.type.value} error: {self.message}"


class CError(OOPLError):
    char_pos: int
    line_number: int
    message: str
    type: OOPLErrorTypes

    def __init__(
        self, type: OOPLErrorTypes, line_number: int, char_pos: int, message: str
    ) -> None:
        super().__init__(type, message)
        self.char_pos = char_pos
        self.line_number = line_number


VMError: TypeAlias = OOPLError
