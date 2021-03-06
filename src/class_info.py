from .var_table import VarTable
from .func_dir import CFuncDir


class ClassInfo:
    name: str
    var_table: VarTable
    funcs: list[str]

    def __init__(self, name: str) -> None:
        self.name = name
        self.var_table = VarTable()
        self.funcs = []
