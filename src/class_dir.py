from src.attribute_info import AttributeInfo

class ClassDir():
    attr_dir: dict[str, AttributeInfo]

    def __init__(self):
        self.class_dir = {}

    
    def get_attr(self, name: str) -> AttributeInfo:
        """
        Return attribute info corresponding to attribute with that name.

        Arguments:
        name: str -- Name of the attribute.
        """
        if(attr_info := self.attr_dir.get(name)) is not None:
            return attr_info
        else:
            raise Exception(f"Couldn't retrieve the information of attribute {name}.")
    
    def has_attr(self, name: str) -> bool:
        """
        Check whether a variable is contained in the directory.

        Arguments:
        name: str -- Name of the attribute.
        """
        return False if self.attr_dir.get_attr(name) is None else True
    
