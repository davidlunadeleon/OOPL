from src.attribute_info import AttributeInfo

class classInfo:
    attr_dir: dict[str, AttributeInfo]

class ClassDir():
    class_dir: dict[str, classInfo]

    def __init__(self):
        self.func_dir = {}