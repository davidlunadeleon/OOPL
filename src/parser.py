# OOPL parser

# Import libraries
from .libs.ply import yacc

from .lexer import Lexer
from .utils.types import TokenList
from .var_table import VarTable
from .func_dir import FuncDir
from .utils.enums import Types, Operations
from .semantic_cube import SemanticCube


class Parser:
    tokens: TokenList
    lexer: Lexer
    global_var_table: VarTable
    func_dir: FuncDir
    scope_stack: list[str]
    semantic_cube: SemanticCube

    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.global_var_table = VarTable()
        self.func_dir = FuncDir()
        self.scope_stack = ["global"]
        self.semantic_cube = SemanticCube()

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
        function    : simple_type_id function_parameters register_function LBRACK function_variables RBRACK block
                    | void_id function_parameters register_function LBRACK function_variables RBRACK block
        """
        self.scope_stack.pop()

    def p_register_function(self, p):
        """
        register_function   :
        """
        function_type, function_name = p[-2]
        function_parameters = p[-1]
        self.func_dir.add(function_name, function_type)
        self.scope_stack.append(function_name)
        func_info = self.func_dir.get(function_name)
        for param_type, param_name in function_parameters:
            if func_info is not None:
                func_info["param_table"].add(param_name, param_type, "test")
            else:
                raise Exception("The function information table was not found.")

    def p_function_parameters(self, p):
        """
        function_parameters : LPAREN params RPAREN
                            | LPAREN RPAREN
        """
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = []

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

    def p_type(self, p):
        """
        simple_type     : INT
                        | FLOAT
                        | STRING
                        | BOOL
        composite_type  : ID
                        | FILE
        void            : VOID
        """
        p[0] = p[1]

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
        params  : simple_type_id COMMA params
                | simple_type_id
        """
        if len(p) == 4:
            p[0] = [p[1], *p[3]]
        else:
            p[0] = [p[1]]

    def p_type_id(self, p):
        """
        simple_type_id      : simple_type ID
        composite_type_id   : composite_type ID
        void_id             : void ID
        """
        id_type = p[1]
        id = p[2]
        p[0] = (id_type, id)

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
        var_decl : composite_type ID id_list SEMICOLON
                 | simple_type ID matrix_row SEMICOLON
        """
        var_type = p[1]
        var_names = [p[2], *p[3]]
        scope = self.scope_stack[-1]
        if scope == "global":
            for var_name in var_names:
                self.global_var_table.add(var_name, var_type, "test")
        else:
            func_info = self.func_dir.get(scope)
            if func_info is not None:
                for var_name in var_names:
                    func_info["var_table"].add(var_name, var_type, "test")
            else:
                raise Exception("The function information table was not found.")

    def p_id_list(self, p):
        """
        id_list : COMMA ID id_list
                |
        """
        if len(p) == 4:
            p[0] = [p[2], *p[3]]
        else:
            p[0] = []

    def p_matrix_row(self, p):
        """
        matrix_row  : LBRACK INT_CONSTANT RBRACK matrix_column
                    | simple_id_list
        """
        if len(p) == 5:
            p[0] = p[4]
        else:
            p[0] = p[1]

    def p_matrix_column(self, p):
        """
        matrix_column   :  LBRACK INT_CONSTANT RBRACK simple_id_list
                        |
        """
        if len(p) == 5:
            p[0] = p[4]
        else:
            p[0] = []

    def p_simple_id_list(self, p):
        """
        simple_id_list  :   COMMA ID matrix_row
                        |
        """
        if len(p) == 4:
            p[0] = [p[2], *p[3]]
        else:
            p[0] = []

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
               | constant
        """

    def p_constant(self, p):
        """
        constant    : int_constant
                    | float_constant
                    | string_constant
                    | bool_constant
        """
        p[0] = p[1]

    def p_bool_constant(self, p):
        """
        bool_constant   : BOOL_CONSTANT
        """
        p[0] = (Types.BOOL, p[1])

    def p_string_constant(self, p):
        """
        string_constant : STRING_CONSTANT
        """
        p[0] = (Types.STRING, p[1])

    def p_float_constant(self, p):
        """
        float_constant  : FLOAT_CONSTANT
        """
        p[0] = (Types.FLOAT, p[1])

    def p_int_constant(self, p):
        """
        int_constant    : INT_CONSTANT
        """
        p[0] = (Types.INT, p[1])

    def p_error(self, p):
        # print(f'Syntax error at {p.value!r} in line {p.lineno}')
        print(f"Syntax error at {p} for {p.value!r} in line {p.lineno}")
