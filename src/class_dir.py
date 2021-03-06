from .class_info import ClassInfo
from .containers.dir import Dir


class ClassDir(Dir[ClassInfo]):
    def __init__(self):
        super().__init__()

    def add(self, name: str):
        """
        Inserting a new class into the directory.

        Arguments:
        name: str -- Name of the class to be added.
        """
        if name in self.dir:
            raise Exception(f"The class {name} was already defined.")
        else:
            self.dir[name] = ClassInfo(name)

    def print(self, verbose: bool) -> None:
        """
        Print information of the directory depending on verbose flag value.
        """
        for value in self.values():
            if verbose:
                print(f"# {value.name}")
            value.func_dir.print(verbose)
            value.var_table.print(f"Class {value.name} VarTable", verbose)
