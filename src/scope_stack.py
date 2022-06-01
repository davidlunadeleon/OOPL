from .containers.stack import Stack
from .scope import Scope
from .utils.enums import ScopeTypes
from .var_info import VarInfo


class ScopeStack(Stack[Scope]):
    def __init__(self) -> None:
        super().__init__()

    def has_var(self, var_name: str) -> bool:
        for scope in reversed(self.stack):
            if scope.has(var_name):
                return True
        return False

    def get_var(self, var_name: str) -> VarInfo:
        for scope in reversed(self.stack):
            if scope.has(var_name):
                return scope.get(var_name)
        raise Exception(f"Could not find {var_name}.")

    def is_in_loop(self) -> bool:
        for scope in reversed(self.stack):
            if scope.type is ScopeTypes.LOOP:
                return True
        return False

    def is_in_class(self) -> bool:
        for scope in reversed(self.stack):
            if scope.type is ScopeTypes.CLASS:
                return True
        return False
