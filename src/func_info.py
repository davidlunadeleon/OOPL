from .utils.types import FunctionResources, MemoryAddress, ParamList
from .scope import Scope
from .utils.enums import Types


class FuncInfo:
    start_quad: int
    resources: FunctionResources
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class CFuncInfo(FuncInfo):
    address: MemoryAddress
    has_return: bool
    is_body_defined: bool
    param_list: ParamList
    return_address: MemoryAddress | None
    scope: Scope
    type: Types

    def __init__(
        self,
        name: str,
        return_address: MemoryAddress | None,
        scope: Scope,
        type: Types,
        address: MemoryAddress,
    ) -> None:
        super().__init__(name)
        self.address = address
        self.has_return = False
        self.is_body_defined = False
        self.param_list = []
        self.resources = (0, 0, 0, 0, 0)
        self.return_address = return_address
        self.scope = scope
        self.type = type


class VMFuncInfo(FuncInfo):
    def __init__(
        self,
        name: str,
        start_quad: int,
        resources: FunctionResources,
    ) -> None:
        super().__init__(name)
        self.start_quad = start_quad
        self.resources = resources
