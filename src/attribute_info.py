from .utils.enums import Types
from src.array_info import ArrayInfo

class AttributeInfo:
    name: str
    type: Types
    array_info: ArrayInfo | None