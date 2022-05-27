from enum import Enum


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
    FUNCTION = "function"
    GENERIC = "generic"
    GLOBAL = "global"
    LOOP = "loop"


class Segments(Enum):
    FUNCTIONS = "%%functions"
    GLOBAL_MEMORY = "%%global_memory"
    GLOBAL_RESOURCES = "%%global_resources"
    QUADRUPLES = "%%quadruples"
