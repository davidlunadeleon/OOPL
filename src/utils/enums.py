import enum

class Types(enum.Enum):
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string'
    BOOL = 'bool'

class Operations(enum.Enum):
    PLUS = '+'
    MINUS = '-'
    DIVIDES = '/'
    TIMES = '*'
    GT = '>'
    EQGT = '>='
    LT = '<'
    EQLT = '<='
    EQ = '=='
    DIFF = '!='
    ASSIGN = '='
    OR = '||'
    AND = '&&'