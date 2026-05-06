# process modules
from enum import Enum, auto

# app modules
from source.script.node import *

class BaseTypes(Enum):
    INT = auto()
    FLOAT = auto()
    STR = auto()
    CHAR = auto()
    BOOL = auto() 
    
    STRUCT = auto()
    SPACE = auto()

class Vts(BaseTypes):
    _structs: dict[str, StructNode] = {}
    _spaces: dict[str, SpaceNode] = {}

    @classmethod
    def set_type(cls, _name: str, _struct: StructNode): cls._structs[_name] = _struct
    @classmethod
    def get_type(cls, _name: str) -> StructNode | None: return cls._structs.get(_name)
    @classmethod
    def has_type(cls, struct_name: str) -> bool: return struct_name in cls._structs

@overload
def to_Vts(t_str: str="") -> BaseTypes: ...

@overload
def to_Vts(t_int: int=0) -> BaseTypes: ...

def to_Vts(t_val: Union[str, int]) -> BaseTypes:
    if isinstance(t_val, str):
        _str = t_val.strip().upper()
        if _str not in BaseTypes.__members__: 
            raise SyntaxError(f"Data type '{t_val}' is not valid.")
        return BaseTypes[_str]

    elif isinstance(t_val, int):
        try: return BaseTypes(t_val)
        except ValueError:
            raise SyntaxError(f"Value '{t_val}' does not match any Vtypes.")

    raise TypeError("t_val must be str or int")
