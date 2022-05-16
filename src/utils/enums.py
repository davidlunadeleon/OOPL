import enum


class Types(enum.Enum):
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"


class Operations(enum.Enum):
    AND = "&&"
    ASSIGNOP = "="
    DIFF = "!="
    DIVIDES = "/"
    EQ = "=="
    EQGT = ">="
    EQLT = "<="
    GT = ">"
    LT = "<"
    MINUS = "-"
    OR = "||"
    PLUS = "+"
    TIMES = "*"
