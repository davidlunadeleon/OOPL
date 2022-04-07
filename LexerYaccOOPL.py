# 
# @file LexerYaccOOPL.py
# @author David Luna and Yulisa Medina
# @brief 
# @version 0.1
# @date 2022-03-07
# 
# @copyright Copyright (c) 2022
#  
#  

from ply import lex
from ply import yacc
import sys

# --- Keywords

keywords = {
    'program' :'PROGRAM',
    'if' : 'IF', 
    'elseif' : 'ELSEIF',
    'else' : 'ELSE', 
    'class' : 'CLASS',
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'string' : 'STRING',
    'void' : 'VOID',
    'print' : 'PRINT',
    'for' : 'FOR',
    'break' : 'BREAK',
    'while' : 'WHILE',
    'return' : 'RETURN',
    'read' : 'READ',
    'main' : 'MAIN',
    'this' : 'THIS',
    'true' : 'TRUE',
    'false' : 'FALSE'  
}

# --- Tokenizer

tokens = list(keywords.values()) + [ 
    'ID', 'INT_CONSTANT', 'FLOAT_CONSTANT', 'BOOL_CONSTANT', 'STRING_CONSTANT',
    'RELOP', 'AND', 'OR',
    'SEMICOLON', 'COLON', 'COMMA', 'DOT', 'LPAREN' ,'RPAREN', 'LBRACK', 'RBRACK', 'LCURBR', 'RCURBR',
    'TIMES', 'DIVIDES', 'PLUS', 'MINUS', 'ASSIGNOP',
    'COMMENT'
]

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_RELOP = r'\<\>|>|<'
t_AND = r'\&\&'
t_OR = r'\|\|'

t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCURBR = r'\{'
t_RCURBR = r'\}'

t_TIMES = r'\*'
t_DIVIDES = r'\/'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_ASSIGNOP = r'\='

t_COMMENT = r'\#.*'

t_INT_CONSTANT = r'[+-]?[0-9]+'
t_FLOAT_CONSTANT = r'[+-]?[0-9]+\.[0-9]+'
t_BOOL_CONSTANT = r'(True|False)'
t_STRING_CONSTANT = r'\".*\"'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_ID(t):
    r'[a-zA-Z]+[a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

# def t_CTEI(t):
#     r'[0-9]+'
#     t.value = int(t.value)
#     return t

# def t_CTEF(t):
#     r'[0-9]+(\.[0-9]+)?'
#     t.value = float(t.value)
#     return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r} in line {t.lineno}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex.lex()
    
# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
def p_s(t):
    '''
    s : PROGRAM ID SEMICOLON s_1 bloque
    '''
    t[0] = "DONE"




def p_error(p):
    # print(f'Syntax error at {p.value!r} in line {p.lineno}')
    print(f'Syntax error at {p} for {p.value!r} in line {p.lineno}')

# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    # To execute lexer and parser, user will add the file to be tested as an argument
    if len(sys.argv) == 2:
        name = sys.argv[1]
        try:
            with open(name, 'r') as file:
                file_content = file.read()
                # Parse an expression
                if parser.parse(file_content) == "DONE":
                    print("Data inputted from file is valid.")
                else:
                    print("Data inputted from file is invalid.")
        except (EOFError, FileNotFoundError) as e:
            print(e)
    else:
        print("Error: Incorrect argument list. Only one filename should be added for testing besides the file that contains the lexer and parser.")