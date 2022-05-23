# OOPL parser

# Import libraries
from .libs.ply import yacc

from .func_dir import FuncDir
from .lexer import Lexer
from .utils.enums import Types, Operations, ScopeTypes
from .utils.types import TokenList
from .quadruple_list import QuadrupleList
from .memory import Memory
from .nodes.constant import Constant
from .nodes.expression import Expression
from .scope_stack import ScopeStack
from .scope import Scope


class Parser:
    func_dir: FuncDir
    function_memory: Memory
    function_stack: list[str]
    global_memory: Memory
    jump_stack: list[int]
    lexer: Lexer
    quads: QuadrupleList
    scope_stack: ScopeStack
    tokens: TokenList

    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.func_dir = FuncDir()
        self.function_memory = Memory(4000)
        self.function_stack = []
        self.global_memory = Memory(0)
        self.jump_stack = []
        self.quads = QuadrupleList()
        self.scope_stack = ScopeStack()
        self.scope_stack.push(Scope(ScopeTypes.GLOBAL, self.global_memory))

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
        for index, quad in enumerate(self.quads.quads):
            op, func_name, _, _ = quad
            if op is Operations.GOSUB:
                if (
                    isinstance(func_name, str)
                    and self.func_dir.has(func_name)
                    and (func_info := self.func_dir.get(func_name))["body_defined"]
                ):
                    bools, floats, ints, strings = func_info["resources"]
                    self.quads[index - 4] = (Operations.ERAB, None, None, bools)
                    self.quads[index - 3] = (Operations.ERAF, None, None, floats)
                    self.quads[index - 2] = (Operations.ERAI, None, None, ints)
                    self.quads[index - 1] = (Operations.ERAS, None, None, strings)
                else:
                    raise Exception(
                        f"Function {func_name} was called but its body was not defined."
                    )
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
        function    : simple_type_id function_parameters register_function mark_function_begin block
                    | void_id function_parameters register_function mark_function_begin block
        """
        func_name = self.function_stack.pop()
        self.scope_stack.pop()
        if (func_info := self.func_dir.get(func_name)) is not None:
            if (
                func_info["type"] is not Types.VOID
                and not func_info["has_return_statement"]
            ):
                raise Exception("Missing return statement for non void function.")
            func_info["resources"] = self.function_memory.describe_resources()

        # Only add if there is no return after and it is the end of the function
        if self.quads[self.quads.ptr - 1][0] != Operations.ENDSUB:
            self.quads.add((Operations.ENDSUB, None, None, None))
        print(func_name)
        self.function_memory.print()
        self.function_memory.clear()

    def p_mark_function_begin(self, p):
        """
        mark_function_begin :
        """
        func_name = self.function_stack[-1]
        func_info = self.func_dir.get(func_name)
        if func_info is not None:
            func_info["start_quad"] = self.quads.ptr

    def p_register_function(self, p):
        """
        register_function   :
        """
        func_type, func_name = p[-2]
        func_params = p[-1]
        return_address = (
            None if func_type is Types.VOID else self.global_memory.reserve(func_type)
        )
        func_info = self.func_dir.add(
            func_name, True, func_type, return_address, self.function_memory
        )
        self.function_stack.append(func_name)
        self.scope_stack.push(func_info["scope"])
        for param_type, param_name in func_params:
            _, var_address = self.scope_stack.add_var(param_name, param_type)
            func_info["param_table"].add(param_name, param_type, var_address)

    def p_function_header(self, p):
        """
        function_header    : simple_type_id function_parameters register_function_header SEMICOLON
                           | void_id function_parameters register_function_header SEMICOLON
        """

    def p_register_function_header(self, p):
        """
        register_function_header   :
        """
        func_type, func_name = p[-2]
        func_parameters = p[-1]
        return_address = (
            None if func_type is Types.VOID else self.global_memory.reserve(func_type)
        )
        func_info = self.func_dir.add(
            func_name, False, func_type, return_address, self.function_memory
        )
        self.scope_stack.push(func_info["scope"])
        for param_type, param_name in func_parameters:
            _, var_address = self.scope_stack.add_var(param_name, param_type)
            func_info["param_table"].add(param_name, param_type, var_address)
        self.scope_stack.pop()

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
        for_loop    : FOR LPAREN for_loop_assign SEMICOLON ptr_to_jump_stack expr loop_expr SEMICOLON ptr_to_jump_stack for_loop_assign RPAREN ptr_to_jump_stack loop_block
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
        for_loop_assign : expr
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
        block           : LCURBR push_scope block_content RCURBR pop_scope
        loop_block      : LCURBR push_loop_scope block_content RCURBR pop_scope
        block_content   : statement block_content
                        |
        statement       : expr SEMICOLON
                        | read
                        | write
                        | if_statement
                        | while_loop
                        | for_loop
                        | break
                        | return SEMICOLON
                        | var_decl
        """

    def p_push_scope(self, p):
        """
        push_scope :
        """
        self.scope_stack.push(Scope(ScopeTypes.GENERIC, self.function_memory))

    def p_push_loop_scope(self, p):
        """
        push_loop_scope :
        """
        self.scope_stack.push(Scope(ScopeTypes.LOOP, self.function_memory))

    def p_pop_scope(self, p):
        """
        pop_scope   :
        """
        self.scope_stack.pop()

    def p_while_loop(self, p):
        """
        while_loop  : WHILE LPAREN ptr_to_jump_stack expr loop_expr RPAREN loop_block
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
        if not self.scope_stack.is_in_loop():
            raise Exception("Can't use break statement outside a loop.")

    def p_return(self, p):
        """
        return  : RETURN expr
        """
        expr_type, expr_address = p[2]
        func_name = self.function_stack[-1]
        if (func_info := self.func_dir.get(func_name)) is not None:
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

    def p_call(self, p):
        """
        call    : ID call_arguments
                | ID DOT ID call_arguments
        """
        if len(p) == 3:
            func_name = p[1]
            func_args = p[2]
            if (func_info := self.func_dir.get(func_name)) is not None:
                self.quads.add((Operations.ERAB, None, None, None))
                self.quads.add((Operations.ERAF, None, None, None))
                self.quads.add((Operations.ERAI, None, None, None))
                self.quads.add((Operations.ERAS, None, None, None))
                param_table = func_info["param_table"]
                if len(func_args) != len(param_table.table.items()):
                    raise Exception(
                        f"Arg, self.function_memoryument mismatch when calling {func_name}."
                    )
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
                        (Operations.GOSUB, func_name, None, func_info["start_quad"])
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
            var_info = self.scope_stack.get_var(p[1])
            if var_info is not None:
                p[0] = var_info
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
        if p[3] is not None:
            _, expr_addr = p[3]
            self.quads.add((Operations.READ, expr_addr, None, None))
        else:
            raise Exception(f"No variable found with the id {p[3]}.")

    def p_write(self, p):
        """
        write : PRINT call_arguments SEMICOLON
        """
        print_args = p[2]
        for print_arg in print_args:
            if print_arg is not None:
                self.quads.add((Operations.PRINT, print_arg[1], None, None))
            else:
                raise Exception(f"No variable found with the id {p[3]}.")

    def p_var_decl(self, p):
        """
        var_decl : composite_type ID id_list SEMICOLON
                 | simple_type ID matrix_row SEMICOLON
        """
        var_type = p[1]
        var_names = [p[2], *p[3]]
        for var_name in var_names:
            self.scope_stack.add_var(var_name, var_type)

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
        expr        : variable ASSIGNOP expr
                    | variable ASSIGNOP or_expr
        or_expr     : or_expr OR and_expr
        and_expr    : and_expr AND comp_expr
        comp_expr   : comp_expr COMPOP rel_expr
        rel_expr    : rel_expr RELOP m_expr
        m_expr      : m_expr PLUS term
                    | m_expr MINUS term
        term        : term DIVIDES factor
                    | term TIMES factor
        """
        p[0] = Expression(
            p[1], Operations(p[2]), p[3], self.function_memory, self.quads
        ).get()

    def p_identity(self, p):
        """
        expr            : or_expr
        or_expr         : and_expr
        and_expr        : comp_expr
        comp_expr       : rel_expr
        rel_expr        : m_expr
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
        p[0] = Constant(p[1], Types.BOOL, self.global_memory).get()

    def p_string_constant(self, p):
        """
        string_constant : STRING_CONSTANT
        """
        p[0] = Constant(p[1], Types.STRING, self.global_memory).get()

    def p_float_constant(self, p):
        """
        float_constant  : FLOAT_CONSTANT
        """
        p[0] = Constant(p[1], Types.FLOAT, self.global_memory).get()

    def p_int_constant(self, p):
        """
        int_constant    : INT_CONSTANT
        """
        p[0] = Constant(p[1], Types.INT, self.global_memory).get()

    def p_error(self, p):
        # print(f'Syntax error at {p.value!r} in line {p.lineno}')
        print(f"Syntax error at {p} for {p.value!r} in line {p.lineno}")
