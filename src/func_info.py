from .utils.types import FunctionResources, MemoryAddress, ParamList
from .scope import Scope


class FuncInfo:
    start_quad: int
    resources: FunctionResources
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __resources_str(self) -> str:
        return str(self.resources).removeprefix("(").removesuffix(")")

    def __str__(self) -> str:
        return f"{self.name},{self.start_quad},{self.__resources_str()}"


class CFuncInfo(FuncInfo):
    address: MemoryAddress
    has_return: bool
    is_body_defined: bool
    param_list: ParamList
    return_address: MemoryAddress | None
    scope: Scope
    type: str

    def __init__(
        self,
        name: str,
        return_address: MemoryAddress | None,
        scope: Scope,
        type: str,
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

    def __str__(self) -> str:
        return super().__str__()


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

    def __str__(self) -> str:
        return super().__str__()
