import enum


class Types(enum.Enum):
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    VOID = "void"


class Operations(enum.Enum):
    AND = "&&"
    ASSIGNOP = "="
    DIFF = "!="
    DIVIDES = "/"
    EQ = "=="
    EQGT = ">="
    EQLT = "<="
    GOTO = "GOTO"
    GOTOF = "GOTOF"
    GOTOT = "GOTOT"
    GT = ">"
    LT = "<"
    MINUS = "-"
    OR = "||"
    PLUS = "+"
    TIMES = "*"
