# process modules
from enum import Enum, auto
from typing import Union

class Vtype():
    def __init__(self, **kwargs: any):
        self.kind = kwargs.get("kind", None)
        self.name = kwargs.get("name", None)


class BaseTypes(Enum):
    NONE = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()
    CHAR = auto()
    BOOL = auto() 

    LIST = auto()
    DICT = auto()

    ANY = auto()

class UDTs():
    _structs: dict[str, any] = dict()

    @classmethod
    def set_type(cls, _name: str, _struct: any): 
        cls._structs[_name] = _struct
    @classmethod
    def get_type(cls, _name: str) -> any: 
        return cls._structs.get(_name)
    @classmethod
    def has_type(cls, struct_name: str) -> bool: 
        return struct_name in cls._structs

Base_ts = 0
Udef_ts = 1

@property
def vts() -> dict[str, Vtype]:
    global Base_ts, Udef_ts
    
    combined = {
        name: Vtype(kind=Base_ts, name=name)
        for name in BaseTypes.__members__.keys()
    }
    
    for name, node in UDTs._structs.items():
        combined[name] = Vtype(kind=Udef_ts, 
            name=name, node=node
        )
        
    return combined
