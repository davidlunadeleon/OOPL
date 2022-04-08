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
    'ID', 'INT_CONSTANT', 'FLOAT_CONSTANT', 'BOOL_CONSTANT', 'STRING_CONSTANT', 'FILE',
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
t_FILE = r'[a-zA-Z]+[a-zA-Z0-9_]\.oopl'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_ID(t):
    r'[a-zA-Z]+[a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

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
def p_program(t):
    '''
    program : class program_1
            | function program_1
            | variable program_1
            |
    '''
    t[0] = "DONE"

def p_program_1(t):
    '''
    program_1 : MAIN LPAREN RPAREN block
              | program
    '''

def p_class(t):
    '''
    class : CLASS ID class_1 LCURBR class_2 RCURBR
    '''

def p_class_1(t):
    '''
    class_1 : COLON ID
            |
    '''
def p_class_2(t):
    '''
    class_2 : var_decl
            | function
    '''

def p_for_loop(t):
    '''
    for_loop : FOR LPAREN for_loop_1 SEMICOLON expr SEMICOLON expr RPAREN block
    '''

def p_for_loop_1(t):
    '''
    for_loop_1 : variable ASSIGNOP expr
               |
    '''

def p_block(t):
    '''
    block : LCURBR block_1 RCURBR
    '''

def p_block_1(t):
    '''
    block_1 : statement
            | var_decl
            |
    '''

def p_while_loop(t):
    '''
    while_loop : WHILE LPAREN expr RPAREN block
    '''

def p_conditional(t):
    '''
    conditional : IF LPAREN expr RPAREN block conditional_1
    '''

def p_conditional_1(t):
    '''
    conditional_1 : ELSEIF LPAREN expr RPAREN block conditional_1
                  | ELSE block
                  |
    '''

def p_var_decl(t):
    '''
    var_decl : composite_type ID var_decl_1 SEMICOLON
             | simple_type ID var_decl_2 SEMICOLON
    '''

def p_var_decl_1(t):
    '''
    var_decl_1 : COMMA ID var_decl_1
              |
    '''

def p_var_decl_2(t):
    '''
    var_decl_2 : COMMA ID var_decl_3
               | LBRACK INT_CONSTANT RBRACK var_decl_3
               |
    '''

def p_var_decl_3(t):
    '''
    var_decl_3 : var_decl_2
                | LBRACK INT_CONSTANT RBRACK var_decl_2
    '''

def p_simple_type(t):
    '''
    simple_type : INT
                | FLOAT
                | STRING
                | BOOL
    '''

def p_composite_type(t):
    '''
    composite_type : ID
                   | FILE
    '''

def p_function(t):
    '''
    function : function_1 ID LPAREN params RPAREN LBRACK function_2 RBRACK block
    '''

def p_function_1(t):
    '''
    function_1 : simple_type
               | VOID
    '''

def p_function_2(t):
    '''
    function_2 : var_decl function_2
               |
    '''

def p_params(t):
    '''
    params : simple_type ID params_1
    '''

def p_params_1(t):
    '''
    params_1 : COMMA params
             |
    '''

def p_statement(t):
    '''
    statement : assign
              | call
              | read
              | write
              | conditional
              | while_loop
              | for_loop
    '''

def p_assign(t):
    '''
    assign : variable ASSIGNOP expr SEMICOLON
    '''

def p_read(t):
    '''
    read : READ LPAREN variable RPAREN SEMICOLON
    '''

def p_write(t):
    '''
    write : PRINT LPAREN write_1 RPAREN SEMICOLON
    '''

def p_write_1(t):
    '''
    write_1 : expr COMMA
            | STRING_CONSTANT COMMA
            | expr
            | STRING_CONSTANT
    '''

def p_variable(t):
    '''
    variable : ID variable_1
    '''

def p_variable_1(t):
    '''
    variable_1 : DOT variable
               | LBRACK expr RBRACK variable_2
    '''

def p_variable_2(t):
    '''
    variable_2 : LBRACK expr RBRACK
               |
    '''

def p_call(t):
    '''
    call : ID call_1
    '''

def p_call_1(t):
    '''
    call_1 : DOT call
           | LPAREN expr call_2 RPAREN SEMICOLON
    '''

def p_call_2(t):
    '''
    call_2 : COMMA expr call_2
           |
    '''

def p_expr(t):
    '''
    expr : t_expr expr_1
    '''

def p_expr_1(t):
    '''
    expr_1 : OR expr
           |
    '''

def p_t_expr(t):
    '''
    t_expr : g_expr t_expr_1
    '''

def p_t_expr_1(t):
    '''
    t_expr_1 : AND t_expr
             |
    '''

def p_g_expr(t):
    '''
    g_expr : m_expr RELOP m_expr
           | m_expr
    '''

def p_m_expr(t):
    '''
    m_expr : term m_expr_1
    '''

def p_m_expr_1(t):
    '''
    m_expr_1 : PLUS
             | MINUS
             |
    '''

def p_term(t):
    '''
    term : factor term_1
    '''

def p_term_1(t):
    '''
    term_1 : DIVIDES
           | TIMES
           |
    '''

def p_factor(t):
    '''
    factor : LPAREN expr RPAREN
           | variable
           | call
           | INT_CONSTANT
           | FLOAT_CONSTANT
           | STRING_CONSTANT
    '''

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
                parser.parse(file_content)
        except (EOFError, FileNotFoundError) as e:
            print(e)
    else:
        print("Error: Incorrect argument list. Only one filename should be added for testing besides the file that contains the lexer and parser.")