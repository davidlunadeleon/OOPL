from enum import Enum, auto

# For functions and variables
class Types(Enum):
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    VOID = "void"
    PTR = "ptr"

# For quadruples and VM's switch execution
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
    OPT_ASSIGN = "OPT_ASSIGN"
    OPT_PARAM = "OPT_PARAM"
    OR = "||"
    PARAM = "PARAM"
    PLUS = "+"
    PRINT = "PRINT"
    READ = "READ"
    SAVEPTR = "SAVEPTR"
    TIMES = "*"
    VER = "VER"

# To check keywords and types of actions permitted
class ScopeTypes(Enum):
    CLASS = auto()
    CLASS_FUNCTION = auto()
    FUNCTION = auto()
    GENERIC = auto()
    GLOBAL = auto()
    LOOP = auto()

# For better readability in VM's output
class Segments(Enum):
    FUNCTIONS = "%%functions"
    GLOBAL_MEMORY = "%%global_memory"
    GLOBAL_RESOURCES = "%%global_resources"
    QUADRUPLES = "%%quadruples"
