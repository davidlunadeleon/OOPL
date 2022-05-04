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
                | COMMENT program
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
        function    : return_type ID function_parameters LBRACK function_variables RBRACK block
        """

    def p_function_parameters(self, p):
        """
        function_parameters : LPAREN params RPAREN
                            | LPAREN RPAREN
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
                    | expr SEMICOLON
                    | read
                    | write
                    | if_statement
                    | while_loop
                    | for_loop
                    | break
                    | return
        """

    def p_break(self, p):
        """
        break   : BREAK SEMICOLON
        """

    def p_return(self, p):
        """
        return  : RETURN expr SEMICOLON
        """

    def p_assign(self, p):
        """
        assign  : variable ASSIGNOP assign
                | assign_expr
        """

    def p_assign_expr(self, p):
        """
        assign_expr : expr SEMICOLON
        """

    def p_params(self, p):
        """
        params  : simple_type ID params_continuation
        """

    def p_params_continuation(self, p):
        """
        params_continuation : COMMA params
                            |
        """

    def p_call(self, p):
        """
        call    : ID call_arguments
                | ID DOT ID call_arguments
        """

    def p_call_arguments(self, p):
        """
        call_arguments  : LPAREN arguments RPAREN
                        | LPAREN RPAREN
        """

    def p_arguments(self, p):
        """
        arguments   : expr arguments_continuation
        """

    def p_arguments_continuation(self, p):
        """
        arguments_continuation  :   COMMA arguments
                                |
        """

    def p_variable(self, p):
        """
        variable : ID variable_continuation
        """

    def p_variable_continuation(self, p):
        """
        variable_continuation   : DOT ID
                                | LBRACK expr RBRACK matrix_index
        """

    def p_matrix_index(self, p):
        """
        matrix_index    : LBRACK expr RBRACK
                        |
        """

    def p_read(self, p):
        """
        read : READ LPAREN variable RPAREN SEMICOLON
        """

    def p_write(self, p):
        """
        write : PRINT call_arguments SEMICOLON
        """

    def p_var_decl(self, p):
        """
        var_decl : composite_type ID id_list SEMICOLON
                 | simple_type ID matrix_row SEMICOLON
        """

    def p_id_list(self, p):
        """
        id_list : COMMA ID id_list
                |
        """

    def p_matrix_row(self, p):
        """
        matrix_row  : LBRACK INT_CONSTANT RBRACK matrix_column
                    | simple_id_list
        """

    def p_matrix_column(self, p):
        """
        matrix_column   :  LBRACK INT_CONSTANT RBRACK simple_id_list
                        |
        """

    def p_simple_id_list(self, p):
        """
        simple_id_list  :   COMMA ID matrix_row
                        |
        """

    def p_expr(self, p):
        """
        expr    : t_expr expr_cycle
        """

    def p_expr_cycle(self, p):
        """
        expr_cycle  : OR expr
                    |
        """

    def p_t_expr(self, p):
        """
        t_expr  : comp_expr t_expr_cycle
        """

    def p_t_expr_cycle(self, p):
        """
        t_expr_cycle    : AND t_expr
                        |
        """

    def p_comp_expr(self, p):
        """
        comp_expr   : g_expr comp_expr_cycle
        """

    def p_comp_expr_cycle(self, p):
        """
        comp_expr_cycle : COMPOP comp_expr
                        |
        """

    def p_g_expr(self, p):
        """
        g_expr : m_expr RELOP m_expr
               | m_expr
        """

    def p_m_expr(self, p):
        """
        m_expr : term m_expr_cycle
        """

    def p_m_expr_cycle(self, p):
        """
        m_expr_cycle    : PLUS m_expr
                        | MINUS m_expr
                        |
        """

    def p_term(self, p):
        """
        term : factor term_cycle
        """

    def p_term_cycle(self, p):
        """
        term_cycle  : DIVIDES term
                    | TIMES term
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

    def p_error(self, p):
        # print(f'Syntax error at {p.value!r} in line {p.lineno}')
        print(f"Syntax error at {p} for {p.value!r} in line {p.lineno}")
