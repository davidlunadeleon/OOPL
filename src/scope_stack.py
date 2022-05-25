from .array_info import ArrayInfo
from .scope import Scope
from .utils.types import TypeAddress
from .utils.enums import Types, ScopeTypes


class ScopeStack:
    scope_stack: list[Scope]

    def __init__(self) -> None:
        self.scope_stack = []

    def push(self, scope: Scope) -> None:
        self.scope_stack.append(scope)

    def pop(self) -> Scope:
        return self.scope_stack.pop()

    def has_var(self, var_name: str) -> bool:
        for scope in reversed(self.scope_stack):
            if scope.has(var_name):
                return True
        return False

    def get_var(self, var_name: str) -> TypeAddress:
        for scope in reversed(self.scope_stack):
            if scope.has(var_name):
                return scope.get(var_name)
        raise Exception(f"Could not find {var_name}.")

    def add_var(
        self, var_name: str, var_type: Types, array_info: ArrayInfo
    ) -> TypeAddress:
        return self.scope_stack[-1].add(var_name, var_type, array_info)

    def is_in_loop(self) -> bool:
        for scope in reversed(self.scope_stack):
            if scope.type is ScopeTypes.LOOP:
                return True
        return False
