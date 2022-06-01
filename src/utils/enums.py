from enum import Enum, auto


class Types(Enum):
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    VOID = "void"
    PTR = "ptr"


class Operations(Enum):
    AND = "&&"
    ASSIGNOP = "="
    DIFF = "!="
    DIVIDES = "/"
    ENDSUB = "ENDSUB"
    EQ = "=="
    EQGT = ">="
    EQLT = "<="
    ERA = "ERA"
    GOSUB = "GOSUB"
    GOTO = "GOTO"
    GOTOF = "GOTOF"
    GOTOT = "GOTOT"
    GT = ">"
    LT = "<"
    MINUS = "-"
    OR = "||"
    PARAM = "PARAM"
    PLUS = "+"
    PRINT = "PRINT"
    READ = "READ"
    SAVEPTR = "SAVEPTR"
    TIMES = "*"
    VER = "VER"


class ScopeTypes(Enum):
    CLASS_FUNCTION = auto()
    FUNCTION = auto()
    GENERIC = auto()
    GLOBAL = auto()
    LOOP = auto()


class Segments(Enum):
    FUNCTIONS = "%%functions"
    GLOBAL_MEMORY = "%%global_memory"
    GLOBAL_RESOURCES = "%%global_resources"
    QUADRUPLES = "%%quadruples"
