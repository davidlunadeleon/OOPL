# OOPL lexer

# Import libraries
from ply import lex


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Keywords definition
    keywords = {
        "bool": "BOOL",
        "break": "BREAK",
        "class": "CLASS",
        "else": "ELSE",
        "elseif": "ELSEIF",
        "false": "FALSE",
        "float": "FLOAT",
        "for": "FOR",
        "if": "IF",
        "int": "INT",
        "main": "MAIN",
        "print": "PRINT",
        "read": "READ",
        "return": "RETURN",
        "string": "STRING",
        "this": "THIS",
        "true": "TRUE",
        "void": "VOID",
        "while": "WHILE",
    }

    # Tokens definition
    tokens = list(keywords.values()) + [
        "ID",
        "INT_CONSTANT",
        "FLOAT_CONSTANT",
        "BOOL_CONSTANT",
        "STRING_CONSTANT",
        "FILE",
        "RELOP",
        "AND",
        "OR",
        "SEMICOLON",
        "COLON",
        "COMMA",
        "DOT",
        "LPAREN",
        "RPAREN",
        "LBRACK",
        "RBRACK",
        "LCURBR",
        "RCURBR",
        "TIMES",
        "DIVIDES",
        "PLUS",
        "MINUS",
        "ASSIGNOP",
        "COMMENT",
    ]

    # Regular expressions and functions for tokens

    # Ignored characters
    t_ignore = " \t"

    # Simple tokens
    t_RELOP = r"<>|>|<"
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
    t_BOOL_CONSTANT = r"(True|False)"
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
