# OOPL parser

# Import libraries
from .libs.ply import yacc

from .array_info import ArrayInfo
from .func_dir import CFuncDir
from .lexer import Lexer
from .memory import Memory
from .nodes.constant import Constant
from .nodes.expression import Expression
from .quadruple_list import QuadrupleList
from .scope import Scope
from .scope_stack import ScopeStack
from .utils.enums import Types, Operations, ScopeTypes, Segments
from .utils.errors import OOPLErrorTypes, CError
from .utils.types import TokenList, MemoryAddress


class Parser:
    break_counter: list[int]
    break_stack: list[int]
    func_dir: CFuncDir
    function_memory: Memory
    function_stack: list[str]
    global_memory: Memory
    jump_stack: list[MemoryAddress]
    lexer: Lexer
    quads: QuadrupleList
    scope_stack: ScopeStack
    tokens: TokenList
    verbose: bool

    def __init__(self, lexer, verbose: bool):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.break_counter = []
        self.break_stack = []
        self.function_memory = Memory(5001)
        self.function_stack = []
        self.global_memory = Memory(1)
        self.jump_stack = []
        self.scope_stack = ScopeStack()
        self.func_dir = CFuncDir()
        self.scope_stack.push(Scope(ScopeTypes.GLOBAL, self.global_memory))
        self.verbose = verbose

        self.quads = QuadrupleList(self.global_memory)
        self.quads.add((Operations.ERA, 0, 0, 0))
        self.quads.add((Operations.GOSUB, 0, 0, 0))

    def parse(self, p):
        self.parser.parse(p, tracking=True)

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
        self.quads.quads[0] = (
            Operations.ERA,
            0,
            0,
            self.func_dir.get("main").address,
        )
        self.quads.quads[1] = (
            Operations.GOSUB,
            0,
            0,
            self.func_dir.get("main").address,
        )
        for quad in self.quads:
            op, _, _, func_addr = quad
            if op is Operations.GOSUB:
                if func_addr is not None and not (
                    (func_name := self.global_memory[func_addr]) is not None
                    and isinstance(func_name, str)
                    and self.func_dir.has(func_name)
                    and self.func_dir.get(func_name).is_body_defined
                ):
                    raise CError(
                        OOPLErrorTypes.IMPLICIT_DECLARATION,
                        p.lineno(0),
                        p.lexpos(0),
                        f"Function {func_name} was called but its body was not defined.",
                    )
        print(Segments.GLOBAL_RESOURCES.value)
        print(
            str(self.global_memory.describe_resources())
            .removeprefix("(")
            .removesuffix(")")
        )
        print(Segments.GLOBAL_MEMORY.value)
        self.global_memory.print(self.verbose)
        print(Segments.FUNCTIONS.value)
        self.func_dir.print(self.verbose)
        print(Segments.QUADRUPLES.value)
        self.quads.print(self.verbose)

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
                    | simple_type_id function_parameters register_function SEMICOLON
                    | void_id function_parameters register_function SEMICOLON

        """
        func_name = self.function_stack.pop()
        self.scope_stack.pop()

        func_info = self.func_dir.get(func_name)

        if len(p) == 6:
            func_info.is_body_defined = True
            if func_info.type is not Types.VOID.value and not func_info.has_return:
                raise CError(
                    OOPLErrorTypes.SEMANTIC,
                    p.lineno(0),
                    p.lexpos(0),
                    "missing return statement for non void function",
                )
            func_info.resources = self.function_memory.describe_resources()

            # Only add if there is no return after and it is the end of the function
            if self.quads[self.quads.ptr_address(-1)][0] != Operations.ENDSUB:
                self.quads.add((Operations.ENDSUB, 0, 0, 0))
            if self.verbose:
                print(f"# Function: {func_name}")
                print(f"# Memory map:")
                self.function_memory.print(True, True)
        elif len(p) == 5 and func_name == "main":
            # Special logic for main function.
            raise Exception("Main function cannot be declared via forward declaration.")
        self.function_memory.clear()

    def p_mark_function_begin(self, p):
        """
        mark_function_begin :
        """
        func_name = self.function_stack[-1]
        self.func_dir.get(func_name).start_quad = self.quads.ptr_address()

    def p_register_function(self, p):
        """
        register_function   :
        """
        func_type, func_name = p[-2]
        func_params = p[-1]

        # Special logic for main function.
        if func_name == "main":
            if func_type is not Types.INT.value:
                raise Exception("Return type of main function must be int.")
            if len(func_params) > 0:
                raise Exception("Main function can't take any parameters.")

        if self.func_dir.has(func_name):
            func_info = self.func_dir.get(func_name)
            if func_type is not func_info.type:
                raise Exception(
                    f"The new function signature of {func_name} does not match the previously defined signature."
                )

            for saved_param, new_param in zip(func_info.param_list, func_params):
                sp_type, sp_addr, sp_name = saved_param
                np_type, np_name = new_param
                if sp_type is not np_type or np_name != sp_name:
                    raise Exception(
                        f"The new function signature of {func_name} does not match the previously defined signature."
                    )
                else:
                    self.function_memory.reserve(sp_type)
            self.scope_stack.push(func_info.scope)
        else:
            return_address = (
                0
                if func_type is Types.VOID.value
                else self.global_memory.reserve(func_type)
            )
            func_scope = Scope(ScopeTypes.FUNCTION, self.function_memory)
            func_info = self.func_dir.add(
                func_name,
                func_type,
                return_address,
                func_scope,
                self.global_memory.append(Types.STRING.value, func_name),
            )
            self.scope_stack.push(func_scope)
            for param_type, param_name in func_params:
                _, var_address, _ = self.scope_stack.add_var(
                    param_name, param_type, None
                )
                func_info.param_list.append((param_type, var_address, param_name))
        self.function_stack.append(func_name)

    def p_empty_list(self, p):
        """
        function_parameters : LPAREN RPAREN
        call_arguments      : LPAREN RPAREN
        id_list             :
        simple_id_list      :
        dimension           :
        constant_dimension  :
        """
        p[0] = []

    def p_for_loop(self, p):
        """
        for_loop    : FOR LPAREN for_loop_assign SEMICOLON expr for_loop_expr SEMICOLON ptr_to_jump_stack for_loop_assign empty_goto RPAREN ptr_to_jump_stack loop_block
        """
        before_block = self.jump_stack.pop()
        second_assign = self.jump_stack.pop()
        before_second_assign = self.jump_stack.pop()
        after_expr_true = self.jump_stack.pop()
        after_expr_false = self.jump_stack.pop()
        before_expr = self.jump_stack.pop()
        self.quads.add((Operations.GOTO, 0, 0, before_second_assign))
        op_code, _, _, _ = self.quads[second_assign]
        self.quads[second_assign] = (op_code, 0, 0, before_expr)
        op_code, addr, _, _ = self.quads[after_expr_false]
        self.quads[after_expr_false] = (op_code, addr, 0, self.quads.ptr_address())
        op_code, addr, _, _ = self.quads[after_expr_true]
        self.quads[after_expr_true] = (op_code, addr, 0, before_block)
        self.quads.print(True)

    def p_for_loop_assign(self, p):
        """
        for_loop_assign : expr
                        |
        """
        self.jump_stack.append(self.quads.ptr_address())
        print(self.quads.ptr)
        print(self.jump_stack[-1])

    def p_empty_goto(self, p):
        """
        empty_goto  :
        """
        self.quads.add((Operations.GOTO, 0, 0, 0))

    def p_loop_expr(self, p):
        """
        loop_expr  :
        """
        expr_type, expr_addr, _ = p[-1]
        if expr_type is Types.BOOL.value:
            self.jump_stack.append(self.quads.ptr_address())
            self.quads.add((Operations.GOTOF, expr_addr, 0, 0))
        else:
            raise TypeError("Non boolean expression found in loop.")

    def p_for_loop_expr(self, p):
        """
        for_loop_expr  :
        """
        expr_type, expr_addr, _ = p[-1]
        if expr_type is Types.BOOL.value:
            self.jump_stack.append(self.quads.ptr_address())
            self.quads.add((Operations.GOTOF, expr_addr, 0, 0))
            self.jump_stack.append(self.quads.ptr_address())
            self.quads.add((Operations.GOTOT, expr_addr, 0, 0))
        else:
            raise TypeError("Non boolean expression found in loop.")

    def p_no_action(self, p):
        """
        block           : LCURBR push_scope block_content RCURBR pop_scope
        loop_block      : LCURBR push_loop_scope block_content RCURBR pop_loop_scope
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
        self.break_counter.append(0)

    def p_pop_loop_scope(self, p):
        """
        pop_loop_scope   :
        """
        self.scope_stack.pop()
        for _ in range(self.break_counter.pop()):
            self.quads[self.break_stack.pop()] = (
                Operations.GOTO,
                0,
                0,
                self.quads.ptr_address(1),
            )

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
        self.quads.add((Operations.GOTO, 0, 0, before_expr))
        op_code, addr, _, _ = self.quads[after_expr]
        self.quads[after_expr] = (op_code, addr, 0, self.quads.ptr_address())

    def p_ptr_to_jump_stack(self, p):
        """
        ptr_to_jump_stack  :
        """
        self.jump_stack.append(self.quads.ptr_address())

    def p_if_statement(self, p):
        """
        if_statement    : IF LPAREN expr loop_expr RPAREN block push_loop_scope if_alternative pop_loop_scope
        """
        end = self.jump_stack.pop()
        op_code, addr, _, _ = self.quads[end]
        self.quads[end] = (op_code, addr, 0, self.quads.ptr_address())

    def p_if_alternative(self, p):
        """
        if_alternative  : ELSEIF LPAREN if_alternative_neural_point_2 expr loop_expr RPAREN block if_alternative
                        | ELSE if_alternative_neural_point_4 block
                        |
        """

    def p_if_alternative_neural_point_2(self, p):
        """
        if_alternative_neural_point_2  :
        """
        self.break_counter[-1] += 1
        self.break_stack.append(self.quads.ptr_address())
        self.quads.add((Operations.GOTO, 0, 0, 0))
        false = self.jump_stack.pop()
        op_code, addr, _, _ = self.quads[false]
        self.quads[false] = (op_code, addr, 0, self.quads.ptr_address())

    def p_if_alternative_neural_point_4(self, p):
        """
        if_alternative_neural_point_4  :
        """
        self.quads.add((Operations.GOTO, 0, 0, 0))
        false = self.jump_stack.pop()
        self.jump_stack.append(self.quads.ptr_address(-1))
        op_code, addr, _, _ = self.quads[false]
        self.quads[false] = (op_code, addr, 0, self.quads.ptr_address())

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
        p[0] = Types(p[1]).value

    def p_break(self, p):
        """
        break   : BREAK SEMICOLON
        """
        if not self.scope_stack.is_in_loop():
            raise Exception("Can't use break statement outside a loop.")
        self.break_stack.append(self.quads.ptr_address())
        self.quads.add((Operations.GOTO, 0, 0, 0))
        self.break_counter[-1] += 1

    def p_return(self, p):
        """
        return  : RETURN expr
        """
        expr_type, expr_address, _ = p[2]
        func_name = self.function_stack[-1]
        if self.func_dir.has(func_name):
            func_info = self.func_dir.get(func_name)
            if func_info.type is Types.VOID.value:
                raise Exception("Can't return from a void function.")
            elif func_info.return_address is not None and expr_type is func_info.type:
                self.quads.add(
                    (
                        Operations.ASSIGNOP,
                        expr_address,
                        0,
                        func_info.return_address,
                    )
                )
                self.quads.add((Operations.ENDSUB, 0, 0, 0))
                func_info.has_return = True
            else:
                raise CError(
                    OOPLErrorTypes.TYPE_MISMATCH,
                    p.lineno(2),
                    p.lexpos(2),
                    f"function {func_info.name} expected return type {func_info.type} but received {expr_type.value}.",
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
        void_id             : void ID
        """
        # composite_type_id   : composite_type ID
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
            if func_name == "main":
                raise Exception(f"Main function cannot be called.")
            if self.func_dir.has(func_name):
                func_info = self.func_dir.get(func_name)
                param_list = func_info.param_list
                if len(func_args) != len(param_list):
                    raise Exception(
                        f"Arg, self.function_memoryument mismatch when calling {func_name}."
                    )
                else:
                    self.quads.add((Operations.ERA, 0, 0, func_info.address))
                    for arg, param in zip(func_args, param_list):
                        p_type, p_addr, p_name = param
                        arg_type, arg_addr, _ = arg
                        if (
                            p_type is arg_type
                            or (
                                p_type is Types.INT.value
                                and arg_type is Types.FLOAT.value
                            )
                            or (
                                p_type is Types.FLOAT.value
                                and arg_type is Types.INT.value
                            )
                        ):
                            self.quads.add((Operations.PARAM, arg_addr, 0, p_addr))
                        else:
                            raise TypeError(
                                f"Wrong parameter {p_name} in call to {func_name}. Expected {p_type} but received {arg_type}."
                            )
                    self.quads.add((Operations.GOSUB, 0, 0, func_info.address))
                    if func_info.type is not Types.VOID.value:
                        var_addr = self.function_memory.reserve(func_info.type)
                        self.quads.add(
                            (
                                Operations.ASSIGNOP,
                                func_info.return_address,
                                0,
                                var_addr,
                            )
                        )
                    else:
                        var_addr = func_info.return_address
                    p[0] = (func_info.type, var_addr, None)
            else:
                raise Exception(f"Function {func_name} has not been declared.")
        else:
            pass

    def p_variable(self, p):
        """
        variable    : ID DOT ID
                    | ID dimension
        """
        if len(p) == 4:
            pass
        else:
            var_info = self.scope_stack.get_var(p[1])
            if len(p[2]) == 0 and var_info.array_info is None:
                p[0] = (var_info.type, var_info.address, var_info.name)
            elif (array_info := var_info.array_info) is not None and len(p[2]) == len(
                array_info.table
            ):
                _, lower_lim_addr, _ = Constant(
                    "0", Types.INT.value, self.global_memory
                ).get()
                _, addres_address, _ = Constant(
                    str(var_info.address), Types.INT.value, self.global_memory
                ).get()

                addr_stack = []
                for index, (dim, param) in enumerate(zip(array_info.table, p[2])):
                    param_type, param_address, _ = param
                    addr_stack.append(param_address)
                    if not (
                        param_type is Types.INT.value or param_type is Types.FLOAT.value
                    ):
                        raise Exception(
                            f"Can't index {var_info.name} with non int numeric expression."
                        )
                    else:
                        _, upper_lim_addr, _ = Constant(
                            str(dim.lim_s), Types.INT.value, self.global_memory
                        ).get()
                        _, m_addr, _ = Constant(
                            str(dim.m), Types.INT.value, self.global_memory
                        ).get()
                        self.quads.add(
                            (
                                Operations.VER,
                                param_address,
                                lower_lim_addr,
                                upper_lim_addr,
                            )
                        )
                        if index < len(array_info.table) - 1:
                            temp_addr1 = self.function_memory.reserve(Types.INT.value)
                            self.quads.add(
                                (Operations.TIMES, addr_stack.pop(), m_addr, temp_addr1)
                            )
                            addr_stack.append(temp_addr1)
                        if index > 0:
                            temp_addr2 = addr_stack.pop()
                            temp_addr1 = addr_stack.pop()
                            temp_addr3 = self.function_memory.reserve(Types.INT.value)
                            self.quads.add(
                                (Operations.PLUS, temp_addr1, temp_addr2, temp_addr3)
                            )
                            addr_stack.append(temp_addr3)

                temp_addr1 = self.function_memory.reserve(Types.INT.value)
                self.quads.add(
                    (Operations.PLUS, addr_stack.pop(), addres_address, temp_addr1)
                )
                temp_addr2 = self.function_memory.reserve(Types.PTR.value)
                self.quads.add((Operations.SAVEPTR, temp_addr1, 0, temp_addr2))
                p[0] = (var_info.type, temp_addr2, var_info.name)
            else:
                # Variable has dimensions there's a mismatch with the dimensions passed.
                raise Exception(
                    f"Wrong indexing when trying to access {var_info.name}."
                )

    def p_read(self, p):
        """
        read : READ LPAREN variable RPAREN SEMICOLON
        """
        if p[3] is not None:
            _, expr_addr, _ = p[3]
            self.quads.add((Operations.READ, 0, 0, expr_addr))
        else:
            raise Exception(f"No variable found with the id {p[3]}.")

    def p_write(self, p):
        """
        write : PRINT call_arguments SEMICOLON
        """
        print_args = p[2]
        for print_arg in print_args:
            if print_arg is not None:
                self.quads.add((Operations.PRINT, print_arg[1], 0, 0))
            else:
                raise Exception(f"No variable found with the id {p[3]}.")

    def p_var_decl(self, p):
        """
        var_decl : composite_type ID id_list SEMICOLON
                 | simple_type ID constant_dimension simple_id_list SEMICOLON
        """
        var_type = p[1]
        if len(p) == 5:
            var_names = [p[2], *p[3]]
            for var_name in var_names:
                pass
        else:
            var_names = [(p[2], p[3]), *p[4]]
            for var_name, dimensions in var_names:
                array_info = ArrayInfo()
                for _, index, _ in dimensions:
                    value = int(self.global_memory[index])
                    array_info.add_dim(value)
                array_info.update_dims()
                self.scope_stack.add_var(
                    var_name, var_type, None if array_info.size == 0 else array_info
                )

    def p_dimension(self, p):
        """
        dimension   : LBRACK expr RBRACK dimension
        """
        p[0] = [p[2], *p[4]]

    def p_constant_dimension(self, p):
        """
        constant_dimension  : LBRACK int_constant RBRACK constant_dimension
        """
        p[0] = [p[2], *p[4]]

    def p_id_list(self, p):
        """
        id_list : COMMA ID id_list
        """
        p[0] = [p[2], *p[3]]

    def p_simple_id_list(self, p):
        """
        simple_id_list  :   COMMA ID constant_dimension simple_id_list
        """
        p[0] = [(p[2], p[3]), *p[4]]

    def p_operators(self, p):
        """
        expr        : or_expr ASSIGNOP expr
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
            p[1],
            Operations(p[2]),
            p[3],
            self.function_memory,
            self.quads,
            self.scope_stack,
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
        p[0] = Constant(p[1], Types.BOOL.value, self.global_memory).get()

    def p_string_constant(self, p):
        """
        string_constant : STRING_CONSTANT
        """
        p[0] = Constant(p[1], Types.STRING.value, self.global_memory).get()

    def p_float_constant(self, p):
        """
        float_constant  : FLOAT_CONSTANT
        """
        p[0] = Constant(p[1], Types.FLOAT.value, self.global_memory).get()

    def p_int_constant(self, p):
        """
        int_constant    : INT_CONSTANT
        """
        p[0] = Constant(p[1], Types.INT.value, self.global_memory).get()

    def p_error(self, p):
        raise CError(
            OOPLErrorTypes.SYNTAX,
            p.lineno,
            p.lexpos,
            f"unexpected {p.value}",
        )
