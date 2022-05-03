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
    def p_program(self, p):
        """
        program : class program
                | function program
                | var_decl program
                |
        """
        p[0] = "DONE"

    def p_class(self, p):
        """
        class   : CLASS ID class_inheritance LCURBR class_content RCURBR
        """

    def p_class_inheritance(self, p):
        """
        class_inheritance   : COLON ID
                            |
        """

    def p_class_content(self, p):
        """
        class_content   : var_decl class_content
                        | function class_content
                        |
        """

    def p_function(self, p):
        """
        function    : return_type ID LPAREN params RPAREN LBRACK function_variables RBRACK block
        """

    def p_return_type(self, p):
        """
        return_type : simple_type
                    | VOID
        """

    def p_function_variables(self, p):
        """
        function_variables  : var_decl function_variables
                            |
        """

    def p_for_loop(self, p):
        """
        for_loop    : FOR LPAREN for_loop_init SEMICOLON expr SEMICOLON expr RPAREN block
        """

    def p_for_loop_init(self, p):
        """
        for_loop_init   : variable ASSIGNOP expr
                        |
        """

    def p_block(self, p):
        """
        block   : LCURBR block_content RCURBR
        """

    def p_block_content(self, p):
        """
        block_content   : statement block_content
                        |
        """

    def p_while_loop(self, p):
        """
        while_loop  : WHILE LPAREN expr RPAREN block
        """

    def p_if_statement(self, p):
        """
        if_statement    : IF LPAREN expr RPAREN block if_alternative
        """

    def p_if_alternative(self, p):
        """
        if_alternative  : ELSEIF LPAREN expr RPAREN block if_alternative
                        | ELSE block
                        |
        """

    def p_simple_type(self, p):
        """
        simple_type : INT
                    | FLOAT
                    | STRING
                    | BOOL
        """

    def p_composite_type(self, p):
        """
        composite_type : ID
                       | FILE
        """

    def p_statement(self, p):
        """
        statement   : assign
                    | call
                    | read
                    | write
                    | if_statement
                    | while_loop
                    | for_loop
                    | break
        """

    def p_var_decl(self, p):
        """
        var_decl : composite_type ID var_decl_1 SEMICOLON
                 | simple_type ID var_decl_2 SEMICOLON
        """

    def p_var_decl_1(self, p):
        """
        var_decl_1 : COMMA ID var_decl_1
                  |
        """

    def p_var_decl_2(self, p):
        """
        var_decl_2 : COMMA ID var_decl_3
                   | LBRACK INT_CONSTANT RBRACK var_decl_3
                   |
        """

    def p_var_decl_3(self, p):
        """
        var_decl_3 : var_decl_2
                    | LBRACK INT_CONSTANT RBRACK var_decl_2
        """

    def p_params(self, p):
        """
        params : simple_type ID params_1
        """

    def p_params_1(self, p):
        """
        params_1 : COMMA params
                 |
        """

    def p_assign(self, p):
        """
        assign : variable ASSIGNOP expr SEMICOLON
        """

    def p_read(self, p):
        """
        read : READ LPAREN variable RPAREN SEMICOLON
        """

    def p_write(self, p):
        """
        write : PRINT LPAREN write_1 RPAREN SEMICOLON
        """

    def p_write_1(self, p):
        """
        write_1 : expr COMMA
                | STRING_CONSTANT COMMA
                | expr
                | STRING_CONSTANT
        """

    def p_variable(self, p):
        """
        variable : ID variable_1
        """

    def p_variable_1(self, p):
        """
        variable_1 : DOT variable
                   | LBRACK expr RBRACK variable_2
        """

    def p_variable_2(self, p):
        """
        variable_2 : LBRACK expr RBRACK
                   |
        """

    def p_call(self, p):
        """
        call : ID call_1
        """

    def p_call_1(self, p):
        """
        call_1 : DOT call
               | LPAREN expr call_2 RPAREN SEMICOLON
        """

    def p_call_2(self, p):
        """
        call_2 : COMMA expr call_2
               |
        """

    def p_expr(self, p):
        """
        expr : t_expr expr_1
        """

    def p_expr_1(self, p):
        """
        expr_1 : OR expr
               |
        """

    def p_t_expr(self, p):
        """
        t_expr : g_expr t_expr_1
        """

    def p_t_expr_1(self, p):
        """
        t_expr_1 : AND t_expr
                 |
        """

    def p_g_expr(self, p):
        """
        g_expr : m_expr RELOP m_expr
               | m_expr
        """

    def p_m_expr(self, p):
        """
        m_expr : term m_expr_1
        """

    def p_m_expr_1(self, p):
        """
        m_expr_1 : PLUS
                 | MINUS
                 |
        """

    def p_term(self, p):
        """
        term : factor term_1
        """

    def p_term_1(self, p):
        """
        term_1 : DIVIDES
               | TIMES
               |
        """

    def p_factor(self, p):
        """
        factor : LPAREN expr RPAREN
               | variable
               | call
               | INT_CONSTANT
               | FLOAT_CONSTANT
               | STRING_CONSTANT
               | BOOL_CONSTANT
        """

    def p_break(self, p):
        """
        break   : BREAK SEMICOLON
        """

    def p_error(self, p):
        # print(f'Syntax error at {p.value!r} in line {p.lineno}')
        print(f"Syntax error at {p} for {p.value!r} in line {p.lineno}")
