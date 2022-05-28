from enum import Enum


class OOPLErrorTypes(Enum):
    SYNTAX = "syntax"
    TYPE_MISMATCH = "type mismatch"
    IMPLICIT_DECLARATION = "implicit function declaration"


class OOPLError(Exception):
    char_pos: int
    line_number: int
    message: str
    type: OOPLErrorTypes

    def __init__(
        self, type: OOPLErrorTypes, line_number: int, char_pos: int, message: str
    ) -> None:
        self.line_number = line_number
        self.char_pos = char_pos
        self.message = message
        self.type = type
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.type.value} error: {self.message}"
