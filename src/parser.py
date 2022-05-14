# OOPL parser

# Import libraries
from .libs.ply import yacc

from .lexer import Lexer
from .utils.types import TokenList
from .var_table import VarTable
from .func_dir import FuncDir


class Parser:
    tokens: TokenList
    lexer: Lexer
    global_var_table: VarTable
    type_stack: list[str]
    func_dir: FuncDir

    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.global_var_table = VarTable()
        self.type_stack = []
        self.func_dir = FuncDir()

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
                | call SEMICOLON program
                | finish
        """
        p[0] = "DONE"

    def p_finish(self, p):
        """
        finish  :
        """
        self.global_var_table.print("Global variable table")
        print("\n")
        self.func_dir.print()

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
        function    : simple_type ID register_function function_parameters LBRACK function_variables RBRACK block
                    | void ID register_function function_parameters LBRACK function_variables RBRACK block
        """

    def p_register_function(self, p):
        """
        register_function   :
        """
        function_name = p[-1]
        function_type = self.type_stack.pop()
        self.func_dir.add(function_name, function_type)

    def p_function_parameters(self, p):
        """
        function_parameters : LPAREN params RPAREN
                            | LPAREN RPAREN
        """

    def p_function_variables(self, p):
        """
        function_variables  : var_decl function_variables
                            |
        """

    def p_for_loop(self, p):
        """
        for_loop    : FOR LPAREN for_loop_assign SEMICOLON expr SEMICOLON for_loop_assign RPAREN block
        """

    def p_for_loop_assign(self, p):
        """
        for_loop_assign : variable ASSIGNOP expr
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
        simple_type : INT set_type
                    | FLOAT set_type
                    | STRING set_type
                    | BOOL set_type
        """
        p[0] = p[1]

    def p_composite_type(self, p):
        """
        composite_type : ID set_type
                       | FILE set_type
        """
        p[0] = p[1]

    def p_void(self, p):
        """
        void    : VOID set_type
        """
        p[0] = p[1]

    def p_set_type(self, p):
        """
        set_type    :
        """
        type = p[-1]
        self.type_stack.append(type)

    def p_statement(self, p):
        """
        statement   : assign
                    | expr_semicolon
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
                | variable ASSIGNOP expr_semicolon
        """

    def p_expr_semicolon(self, p):
        """
        expr_semicolon  : expr SEMICOLON
        """

    def p_params(self, p):
        """
        params  : simple_type ID COMMA params
                | simple_type ID
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
        arguments   : expr COMMA arguments
                    | expr
        """

    def p_variable(self, p):
        """
        variable    : ID DOT ID
                    | ID LBRACK expr RBRACK matrix_index
                    | ID
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
        var_decl : composite_type ID reg_var id_list SEMICOLON
                 | simple_type ID reg_var matrix_row end_var_reg SEMICOLON
        """

    def p_end_var_registration(self, p):
        """
        end_var_reg :
        """
        self.type_stack.pop()

    def p_reg_var(self, p):
        """
        reg_var :
        """
        var_name = p[-1]
        var_type = self.type_stack[-1]
        self.global_var_table.add(var_name, var_type, "test")

    def p_id_list(self, p):
        """
        id_list : COMMA ID reg_var id_list
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
        simple_id_list  :   COMMA ID reg_var matrix_row
                        |
        """

    def p_expr(self, p):
        """
        expr    : t_expr OR expr
                | t_expr
        """

    def p_t_expr(self, p):
        """
        t_expr  : comp_expr AND t_expr
                | comp_expr
        """

    def p_comp_expr(self, p):
        """
        comp_expr   : g_expr COMPOP comp_expr
                    | g_expr
        """

    def p_g_expr(self, p):
        """
        g_expr : m_expr RELOP g_expr
               | m_expr
        """

    def p_m_expr(self, p):
        """
        m_expr  : term PLUS m_expr
                | term MINUS m_expr
                | term
        """

    def p_term(self, p):
        """
        term    : factor DIVIDES term
                | factor TIMES term
                | factor
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
