# OOPL lexer

# Import libraries
from .libs.ply import lex

from .utils.types import TokenList


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Keywords definition
    keywords: dict[str, str] = {
        "bool": "BOOL",
        "break": "BREAK",
        "class": "CLASS",
        "else": "ELSE",
        "elseif": "ELSEIF",
        "float": "FLOAT",
        "for": "FOR",
        "if": "IF",
        "int": "INT",
        "print": "PRINT",
        "read": "READ",
        "return": "RETURN",
        "string": "STRING",
        "this": "THIS",
        "void": "VOID",
        "while": "WHILE",
        "True": "BOOL_CONSTANT_TRUE",
        "False": "BOOL_CONSTANT_FALSE",
    }

    # Tokens definition
    tokens: TokenList = list(keywords.values()) + [
        "AND",
        "ASSIGNOP",
        "COLON",
        "COMMA",
        "COMMENT",
        "COMPOP",
        "DIVIDES",
        "DOT",
        "FILE",
        "FLOAT_CONSTANT",
        "ID",
        "INT_CONSTANT",
        "LBRACK",
        "LCURBR",
        "LPAREN",
        "MINUS",
        "OR",
        "PLUS",
        "RBRACK",
        "RCURBR",
        "RELOP",
        "RPAREN",
        "SEMICOLON",
        "STRING_CONSTANT",
        "TIMES",
    ]

    # Regular expressions and functions for tokens

    # Ignored characters
    t_ignore = " \t"

    # Simple tokens
    t_RELOP = r"([<>]=?)"
    t_COMPOP = r"[!=]="
    t_AND = r"&&"
    t_OR = r"\|\|"
    t_SEMICOLON = r";"
    t_COLON = r":"
    t_COMMA = r","
    t_DOT = r"\."
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACK = r"\["
    t_RBRACK = r"\]"
    t_LCURBR = r"\{"
    t_RCURBR = r"\}"
    t_TIMES = r"\*"
    t_DIVIDES = r"\/"
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_ASSIGNOP = r"="
    t_INT_CONSTANT = r"[+-]?[0-9]+"
    t_FLOAT_CONSTANT = r"[+-]?[0-9]+\.[0-9]+"
    t_STRING_CONSTANT = r"\".*\""
    t_FILE = r"[a-zA-Z]+[a-zA-Z0-9_]\.oopl"

    # Complex tokens

    def t_ID(self, t):
        r"[a-zA-Z]+[a-zA-Z0-9_]*"
        t.type = self.keywords.get(t.value, "ID")
        return t

    def t_COMMENT(self, t):
        r"\#.*"
        pass
        # No return value. Just ignore and discard the token.

    # Additional functions

    def t_ignore_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    # Error handler for illegal characters
    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r} in line {t.lineno}")
        t.lexer.skip(1)
