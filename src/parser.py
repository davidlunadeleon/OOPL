# OOPL parser

# Import libraries
from audioop import add
from webbrowser import Opera
from .libs.ply import yacc

from .func_dir import FuncDir
from .lexer import Lexer
from .semantic_cube import SemanticCube
from .utils.enums import Types, Operations
from .utils.types import TokenList
from .var_table import VarTable
from .quadruple_list import QuadrupleList
from .memory import Memory


class Parser:
    func_dir: FuncDir
    global_var_table: VarTable
    lexer: Lexer
    scope_stack: list[str]
    semantic_cube: SemanticCube
    tokens: TokenList
    quads: QuadrupleList
    global_memory: Memory
    function_memory: Memory
    jump_stack: list[int]

    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.func_dir = FuncDir()
        self.global_var_table = VarTable()
        self.scope_stack = ["global"]
        self.semantic_cube = SemanticCube()
        self.quads = QuadrupleList()
        self.global_memory = Memory(0)
        self.function_memory = Memory(4000)
        self.jump_stack = []

    def parse(self, p):
        self.parser.parse(p)

    # Write functions for each grammar rule which is
    # specified in the docstring.
    def p_program(self, p):
        """
        program : class program
                | function program
                | function_header program
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
        self.quads.print()
        self.global_memory.print()

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
        function    : simple_type_id function_parameters register_function LBRACK function_variables RBRACK mark_function_begin block
                    | void_id function_parameters register_function LBRACK function_variables RBRACK mark_function_begin block
        """
        scope = self.scope_stack.pop()
        if (func_info := self.func_dir.get(scope)) is not None:
            if (
                func_info["type"] is not Types.VOID
                and not func_info["has_return_statement"]
            ):
                raise Exception("Missing return statement for non void function.")
            func_info["resources"] = self.function_memory.describe_resources()
        self.function_memory.print()
        self.function_memory.clear()

    def p_mark_function_begin(self, p):
        """
        mark_function_begin :
        """
        scope = self.scope_stack[-1]
        func_info = self.func_dir.get(scope)
        if func_info is not None:
            func_info["start_quad"] = self.quads.ptr

    def p_register_function(self, p):
        """
        register_function   :
        """
        function_type, function_name = p[-2]
        function_parameters = p[-1]
        return_address = (
            None
            if function_type is Types.VOID
            else self.global_memory.reserve(function_type)
        )
        self.func_dir.add(function_name, function_type, return_address)
        self.scope_stack.append(function_name)
        func_info = self.func_dir.get(function_name)
        for param_type, param_name in function_parameters:
            if func_info is not None:
                address = self.function_memory.reserve(Types(param_type))
                func_info["param_table"].add(param_name, param_type, address)
            else:
                raise Exception("The function information table was not found.")

    def p_empty_list(self, p):
        """
        function_parameters : LPAREN RPAREN
        call_arguments      : LPAREN RPAREN
        id_list             :
        matrix_column       :
        simple_id_list      :
        """
        p[0] = []

    def p_for_loop(self, p):
        """
        for_loop    : FOR LPAREN for_loop_assign SEMICOLON ptr_to_jump_stack expr loop_expr SEMICOLON ptr_to_jump_stack for_loop_assign RPAREN ptr_to_jump_stack block
        """
        before_block = self.jump_stack.pop()
        second_assign = self.jump_stack.pop()
        before_second_assign = self.jump_stack.pop()
        after_expr = self.jump_stack.pop()
        before_expr = self.jump_stack.pop()
        first_assign = self.jump_stack.pop()
        self.quads.add((Operations.GOTO, None, None, before_second_assign))
        op_code, _, _, _ = self.quads[second_assign]
        self.quads[second_assign] = (op_code, None, None, before_expr)
        op_code, _, _, _ = self.quads[first_assign]
        self.quads[first_assign] = (op_code, None, None, before_block)
        op_code, addr, _, _ = self.quads[after_expr]
        self.quads[after_expr] = (op_code, addr, None, self.quads.ptr)

    def p_for_loop_assign(self, p):
        """
        for_loop_assign : assign
                        |
        """
        self.jump_stack.append(self.quads.ptr)
        self.quads.add((Operations.GOTO, None, None, None))

    def p_loop_expr(self, p):
        """
        loop_expr  :
        """
        expr_type, expr_addr = p[-1]
        if expr_type is Types.BOOL:
            self.jump_stack.append(self.quads.ptr)
            self.quads.add((Operations.GOTOF, expr_addr, None, None))
        else:
            raise TypeError("Non boolean expression found in loop.")

    def p_no_action(self, p):
        """
        block               : LCURBR block_content RCURBR
        block_content       : statement block_content
                            |
        statement           : assign SEMICOLON
                            | expr SEMICOLON
                            | read
                            | write
                            | if_statement
                            | while_loop
                            | for_loop
                            | break
                            | return SEMICOLON
        function_variables  : var_decl function_variables
                            |
        """

    def p_while_loop(self, p):
        """
        while_loop  : WHILE LPAREN ptr_to_jump_stack expr loop_expr RPAREN block
        """
        after_expr = self.jump_stack.pop()
        before_expr = self.jump_stack.pop()
        self.quads.add((Operations.GOTO, None, None, before_expr))
        op_code, addr, _, _ = self.quads[after_expr]
        self.quads[after_expr] = (op_code, addr, None, self.quads.ptr)

    def p_ptr_to_jump_stack(self, p):
        """
        ptr_to_jump_stack  :
        """
        self.jump_stack.append(self.quads.ptr)

    def p_if_statement(self, p):
        """
        if_statement    : IF LPAREN expr if_statement_neural_point_1 RPAREN block if_alternative
        """
        end = self.jump_stack.pop()
        op_code, addr, _, _ = self.quads[end]
        self.quads[end] = (op_code, addr, None, self.quads.ptr)

    def p_if_statement_neural_point_1(self, p):
        """
        if_statement_neural_point_1    :
        """
        expr_type, expr_addr = p[-1]
        if expr_type is Types.BOOL:
            self.quads.add((Operations.GOTOF, expr_addr, None, None))
            self.jump_stack.append(self.quads.ptr - 1)
        else:
            raise TypeError("Type-mismatch of operands.")

    def p_if_alternative(self, p):
        """
        if_alternative  : ELSEIF LPAREN if_alternative_neural_point_2 expr if_alternative_neural_point_3 RPAREN block if_alternative
                        | ELSE if_alternative_neural_point_4 block
                        |
        """

    def p_if_alternative_neural_point_2(self, p):
        """
        if_alternative_neural_point_2  :
        """
        false = self.jump_stack.pop()
        op_code, addr, _, _ = self.quads[false]
        self.quads[false] = (op_code, addr, None, self.quads.ptr)

    def p_if_alternative_neural_point_3(self, p):
        """
        if_alternative_neural_point_3  :
        """
        expr_type, expr_addr = p[-1]
        if expr_type is Types.BOOL:
            self.quads.add((Operations.GOTOF, expr_addr, None, None))
            self.jump_stack.append(self.quads.ptr - 1)
        else:
            raise TypeError("Type-mismatch of operands.")

    def p_if_alternative_neural_point_4(self, p):
        """
        if_alternative_neural_point_4  :
        """
        self.quads.add((Operations.GOTO, None, None, None))
        false = self.jump_stack.pop()
        self.jump_stack.append(self.quads.ptr - 1)
        op_code, addr, _, _ = self.quads[false]
        self.quads[false] = (op_code, addr, None, self.quads.ptr)

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
        p[0] = Types(p[1])

    def p_break(self, p):
        """
        break   : BREAK SEMICOLON
        """

    def p_return(self, p):
        """
        return  : RETURN expr
        """
        expr_type, expr_address = p[2]
        scope = self.scope_stack[-1]
        if (func_info := self.func_dir.get(scope)) is not None:
            if func_info["type"] is Types.VOID:
                raise Exception("Can't return from a void function.")
            elif (
                func_info["return_address"] is not None
                and expr_type is func_info["type"]
            ):
                self.quads.add(
                    (
                        Operations.ASSIGNOP,
                        expr_address,
                        None,
                        func_info["return_address"],
                    )
                )
                self.quads.add((Operations.ENDSUB, None, None, None))
                func_info["has_return_statement"] = True
            else:
                raise TypeError(
                    f'Expected return type {func_info["type"]} but received {expr_type}.'
                )
        else:
            raise Exception("Can't return from outside a function.")

    def p_type_addr_list(self, p):
        """
        params      : simple_type_id COMMA params
                    | simple_type_id
        arguments   : expr COMMA arguments
                    | expr
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
    
    def p_function_header(self, p):
        """
        function_header    : simple_type_id function_parameters SEMICOLON
                           | void_id function_parameters SEMICOLON
        """


    def p_call(self, p):
        """
        call    : ID call_arguments
                | ID DOT ID call_arguments
        """
        if len(p) == 3:
            func_name = p[1]
            func_args = p[2]
            if (func_info := self.func_dir.get(func_name)) is not None and (
                func_resources := func_info["resources"]
            ) is not None:
                func_bools, func_floats, func_ints, func_strings = func_resources
                self.quads.add((Operations.ERAB, None, None, func_bools))
                self.quads.add((Operations.ERAF, None, None, func_floats))
                self.quads.add((Operations.ERAI, None, None, func_ints))
                self.quads.add((Operations.ERAS, None, None, func_strings))
                param_table = func_info["param_table"]
                if len(func_args) != len(param_table.table.items()):
                    raise Exception(f"Argument mismatch when calling {func_name}.")
                else:
                    for arg, param in zip(func_args, param_table.table.items()):
                        _, param_info = param
                        param_type = param_info["type"]
                        param_addr = param_info["address"]
                        param_name = param_info["name"]
                        arg_type, arg_addr = arg
                        if param_type is arg_type:
                            self.quads.add(
                                (Operations.PARAM, arg_addr, None, param_addr)
                            )
                        else:
                            raise TypeError(
                                f"Wrong parameter {param_name} in call to {func_name}. Expected {param_type} but received {arg_type}."
                            )
                    self.quads.add(
                        (Operations.GOSUB, None, None, func_info["start_quad"])
                    )
                    p[0] = (func_info["type"], func_info["return_address"])
            else:
                raise Exception(f"Function {func_name} has not been declared.")
        else:
            pass

    def p_variable(self, p):
        """
        variable    : ID DOT ID
                    | ID LBRACK expr RBRACK matrix_index
                    | ID
        """
        if len(p) == 2:
            scope = self.scope_stack[-1]
            var_info = None
            if (func_info := self.func_dir.get(scope)) is not None:
                var_info = func_info["var_table"].get(p[1]) or func_info[
                    "param_table"
                ].get(p[1])
            if var_info is None:
                var_info = self.global_var_table.get(p[1])
            if var_info is not None:
                p[0] = (var_info["type"], var_info["address"])
        else:
            pass

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
        print_args = p[2]
        for print_arg in print_args:
            self.quads.add((Operations.PRINT, print_arg[1], None, None))


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
                address = self.global_memory.reserve(Types(var_type))
                self.global_var_table.add(var_name, var_type, address)
        else:
            func_info = self.func_dir.get(scope)
            if func_info is not None:
                for var_name in var_names:
                    address = self.function_memory.reserve(Types(var_type))
                    func_info["var_table"].add(var_name, var_type, address)
            else:
                raise Exception("The function information table was not found.")

    def p_id_list(self, p):
        """
        id_list : COMMA ID id_list
        """
        p[0] = [p[2], *p[3]]

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
        """
        p[0] = p[4]

    def p_simple_id_list(self, p):
        """
        simple_id_list  :   COMMA ID matrix_row
        """
        p[0] = [p[2], *p[3]]

    def p_operators(self, p):
        """
        assign      : variable ASSIGNOP assign
                    | variable ASSIGNOP expr
        expr        : expr OR t_expr
        t_expr      : t_expr AND comp_expr
        comp_expr   : comp_expr COMPOP g_expr
        g_expr      : g_expr RELOP m_expr
        m_expr      : m_expr PLUS term
                    | m_expr MINUS term
        term        : term DIVIDES factor
                    | term TIMES factor
        """
        l_type, l_addr = p[1]
        r_type, r_addr = p[3]
        operation = Operations(p[2])
        result_type = self.semantic_cube.get(l_type, operation, r_type)
        if operation is Operations.ASSIGNOP:
            self.quads.add((operation, r_addr, None, l_addr))
            p[0] = (result_type, l_addr)
        else:
            mem_address = self.function_memory.reserve(result_type)
            self.quads.add((operation, l_addr, r_addr, mem_address))
            p[0] = (result_type, mem_address)

    def p_identity(self, p):
        """
        expr            : t_expr
        t_expr          : comp_expr
        comp_expr       : g_expr
        g_expr          : m_expr
        m_expr          : term
        term            : factor
        constant        : int_constant
                        | float_constant
                        | string_constant
                        | bool_constant
        factor          : constant
                        | variable
                        | call
        """
        p[0] = p[1]

    def p_take_second(self, p):
        """
        factor              : LPAREN expr RPAREN
        function_parameters : LPAREN params RPAREN
        call_arguments      : LPAREN arguments RPAREN
        """
        p[0] = p[2]

    def p_bool_constant(self, p):
        """
        bool_constant   : BOOL_CONSTANT_TRUE
                        | BOOL_CONSTANT_FALSE
        """
        val = True if p[1] == "True" else False
        address = self.global_memory.find(val)
        if address is None:
            address = self.global_memory.append(val)
        p[0] = (Types.BOOL, address)

    def p_string_constant(self, p):
        """
        string_constant : STRING_CONSTANT
        """
        val = str(p[1])
        address = self.global_memory.find(val)
        if address is None:
            address = self.global_memory.append(val)
        p[0] = (Types.STRING, address)

    def p_float_constant(self, p):
        """
        float_constant  : FLOAT_CONSTANT
        """
        val = float(p[1])
        address = self.global_memory.find(val)
        if address is None:
            address = self.global_memory.append(val)
        p[0] = (Types.FLOAT, address)

    def p_int_constant(self, p):
        """
        int_constant    : INT_CONSTANT
        """
        val = int(p[1])
        address = self.global_memory.find(val)
        if address is None:
            address = self.global_memory.append(val)
        p[0] = (Types.INT, address)

    def p_error(self, p):
        # print(f'Syntax error at {p.value!r} in line {p.lineno}')
        print(f"Syntax error at {p} for {p.value!r} in line {p.lineno}")
