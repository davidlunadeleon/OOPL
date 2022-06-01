from .class_info import ClassInfo
from .dir import Dir


class ClassDir(Dir[ClassInfo]):
    def __init__(self):
        super().__init__()

    def add(self, name: str):
        if name in self.dir:
            raise Exception(f"The class {name} was already defined.")
        else:
            self.dir[name] = ClassInfo(name)

    def print(self, verbose: bool) -> None:
        for value in self.values():
            if verbose:
                print(f"# {value.name}")
            value.func_dir.print(verbose)
            value.var_table.print(f"Class {value.name} VarTable", verbose)
