from enum import Enum


class Types(Enum):
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    VOID = "void"


class Operations(Enum):
    AND = "&&"
    ASSIGNOP = "="
    DIFF = "!="
    DIVIDES = "/"
    ENDSUB = "ENDSUB"
    EQ = "=="
    EQGT = ">="
    EQLT = "<="
    ERAB = "ERAB"
    ERAF = "ERAF"
    ERAI = "ERAI"
    ERAS = "ERAS"
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
    TIMES = "*"
    PRINT = "PRINT"
    READ = "READ"


class ScopeTypes(Enum):
    GLOBAL = "global"
    FUNCTION = "function"
    LOOP = "loop"
    GENERIC = "generic"


class Segments(Enum):
    GLOBAL_MEMORY = "%%global_memory"
    FUNCTIONS = "%%functions"
    QUADRUPLES = "%%quadruples"
