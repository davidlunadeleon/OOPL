from src.attribute_info import AttributeInfo

class classInfo:
    attr_dir: dict[str, AttributeInfo]

class ClassDir():
    class_dir: dict[str, classInfo]

    def __init__(self):
        self.class_dir = {}
    
    def has_var(self, name: str) -> bool:
        """
        Check whether a variable is contained in the directory.

        Arguments:
        name: str -- Name of the variable.
        """
        return False is self.