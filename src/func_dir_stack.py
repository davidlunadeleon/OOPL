from .containers.stack import Stack
from .func_dir import CFuncDir
from .func_info import CFuncInfo


class FuncDirStack(Stack[CFuncDir]):
    def __init__(self) -> None:
        super().__init__()

    def has_func(self, func_name: str) -> bool:
        for c_func_dir in reversed(self.stack):
            if c_func_dir.has(func_name):
                return True
        return False

    def get_func(self, func_name: str) -> CFuncInfo:
        for c_func_dir in reversed(self.stack):
            if c_func_dir.has(func_name):
                return c_func_dir.get(func_name)
        raise Exception(f"Could not find {func_name}.")
