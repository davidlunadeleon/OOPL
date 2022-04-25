# OOPL parser

# Import libraries
from .libs.ply import yacc


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, p):
        self.parser.parse(p)

    # Write functions for each grammar rule which is
    # specified in the docstring.
    def p_program(self, t):
        """
        program : class program_1
                | function program_1
                | variable program_1
                |
        """
        t[0] = "DONE"

    def p_program_1(self, t):
        """
        program_1 : MAIN LPAREN RPAREN block
                  | program
        """

    def p_class(self, t):
        """
        class : CLASS ID class_1 LCURBR class_2 RCURBR
        """

    def p_class_1(self, t):
        """
        class_1 : COLON ID
                |
        """

    def p_class_2(self, t):
        """
        class_2 : var_decl
                | function
        """

    def p_for_loop(self, t):
        """
        for_loop : FOR LPAREN for_loop_1 SEMICOLON expr SEMICOLON expr RPAREN block
        """

    def p_for_loop_1(self, t):
        """
        for_loop_1 : variable ASSIGNOP expr
                   |
        """

    def p_block(self, t):
        """
        block : LCURBR block_1 RCURBR
        """

    def p_block_1(self, t):
        """
        block_1 : statement
                | var_decl
                |
        """

    def p_while_loop(self, t):
        """
        while_loop : WHILE LPAREN expr RPAREN block
        """

    def p_conditional(self, t):
        """
        conditional : IF LPAREN expr RPAREN block conditional_1
        """

    def p_conditional_1(self, t):
        """
        conditional_1 : ELSEIF LPAREN expr RPAREN block conditional_1
                      | ELSE block
                      |
        """

    def p_var_decl(self, t):
        """
        var_decl : composite_type ID var_decl_1 SEMICOLON
                 | simple_type ID var_decl_2 SEMICOLON
        """

    def p_var_decl_1(self, t):
        """
        var_decl_1 : COMMA ID var_decl_1
                  |
        """

    def p_var_decl_2(self, t):
        """
        var_decl_2 : COMMA ID var_decl_3
                   | LBRACK INT_CONSTANT RBRACK var_decl_3
                   |
        """

    def p_var_decl_3(self, t):
        """
        var_decl_3 : var_decl_2
                    | LBRACK INT_CONSTANT RBRACK var_decl_2
        """

    def p_simple_type(self, t):
        """
        simple_type : INT
                    | FLOAT
                    | STRING
                    | BOOL
        """

    def p_composite_type(self, t):
        """
        composite_type : ID
                       | FILE
        """

    def p_function(self, t):
        """
        function : function_1 ID LPAREN params RPAREN LBRACK function_2 RBRACK block
        """

    def p_function_1(self, t):
        """
        function_1 : simple_type
                   | VOID
        """

    def p_function_2(self, t):
        """
        function_2 : var_decl function_2
                   |
        """

    def p_params(self, t):
        """
        params : simple_type ID params_1
        """

    def p_params_1(self, t):
        """
        params_1 : COMMA params
                 |
        """

    def p_statement(self, t):
        """
        statement : assign
                  | call
                  | read
                  | write
                  | conditional
                  | while_loop
                  | for_loop
        """

    def p_assign(self, t):
        """
        assign : variable ASSIGNOP expr SEMICOLON
        """

    def p_read(self, t):
        """
        read : READ LPAREN variable RPAREN SEMICOLON
        """

    def p_write(self, t):
        """
        write : PRINT LPAREN write_1 RPAREN SEMICOLON
        """

    def p_write_1(self, t):
        """
        write_1 : expr COMMA
                | STRING_CONSTANT COMMA
                | expr
                | STRING_CONSTANT
        """

    def p_variable(self, t):
        """
        variable : ID variable_1
        """

    def p_variable_1(self, t):
        """
        variable_1 : DOT variable
                   | LBRACK expr RBRACK variable_2
        """

    def p_variable_2(self, t):
        """
        variable_2 : LBRACK expr RBRACK
                   |
        """

    def p_call(self, t):
        """
        call : ID call_1
        """

    def p_call_1(self, t):
        """
        call_1 : DOT call
               | LPAREN expr call_2 RPAREN SEMICOLON
        """

    def p_call_2(self, t):
        """
        call_2 : COMMA expr call_2
               |
        """

    def p_expr(self, t):
        """
        expr : t_expr expr_1
        """

    def p_expr_1(self, t):
        """
        expr_1 : OR expr
               |
        """

    def p_t_expr(self, t):
        """
        t_expr : g_expr t_expr_1
        """

    def p_t_expr_1(self, t):
        """
        t_expr_1 : AND t_expr
                 |
        """

    def p_g_expr(self, t):
        """
        g_expr : m_expr RELOP m_expr
               | m_expr
        """

    def p_m_expr(self, t):
        """
        m_expr : term m_expr_1
        """

    def p_m_expr_1(self, t):
        """
        m_expr_1 : PLUS
                 | MINUS
                 |
        """

    def p_term(self, t):
        """
        term : factor term_1
        """

    def p_term_1(self, t):
        """
        term_1 : DIVIDES
               | TIMES
               |
        """

    def p_factor(self, t):
        """
        factor : LPAREN expr RPAREN
               | variable
               | call
               | INT_CONSTANT
               | FLOAT_CONSTANT
               | STRING_CONSTANT
        """

    def p_error(self, p):
        # print(f'Syntax error at {p.value!r} in line {p.lineno}')
        print(f"Syntax error at {p} for {p.value!r} in line {p.lineno}")
