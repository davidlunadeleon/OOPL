from src.attribute_info import AttributeInfo
# from src.method_info import MethodInfo

class classInfo:
    attr_dir: dict[str, AttributeInfo]
    # met_dir: dict[str, MethodInfo]

class ClassDir():
    class_dir: dict[str, classInfo]

    def __init__(self):
        self.func_dir = {}