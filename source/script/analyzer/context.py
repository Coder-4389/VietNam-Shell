# system modules
import sys, os

# Registry
from source.registry import Reg

# app modules
from source.script.node import *
from source.script.token import *
from source.script.typedef import *

class BaseErr(BaseException):
    def __init__(self, _type: str=None, _info: str=None):
        super().__init__()
        self.err_type = _type; self.err_info = _info

    def __str__(self): return f"[Error] {self.err_type}: {self.err_info}"

class NameErr(BaseErr):
    def __init__(self, _info: str=None): super().__init__("NameError", _info)
class SyntaxErr(BaseErr):
    def __init__(self, _info: str=None): super().__init__("SyntaxError", _info)
class TypeErr(BaseErr):
    def __init__(self, _info: str=None): super().__init__("TypeError", _info)
class UnknowErr(BaseErr):
    def __init__(self, _info: str=None): super().__init__("UnknownError", _info)

class Environment():
    def __init__(self, _name: str="", parent: "SpaceEnv"=None):
        self._name = _name
        self._parent = parent

        self._var: dict[str, BaseNode] = dict()
        self._const: dict[str, BaseNode] = dict()

        self._func: dict[str, FuncNode] = dict()
        self._struct: dict[str, StructNode] = dict()
        self._space: dict[str, SpaceNode] = dict()

    def var_def(self, name: str, _type: Vtype): 
        if name in self._const: raise NameErr("Var name can't be like const name")
        self._var[name] = _type
    def const_def(self, name: str, _type: Vtype):
        if name in self._const: raise NameErr("Const can't change value after defined")
        self._const[name] = _type
    def func_def(self, func: FuncNode): self._func[func.name] = func
    def struct_def(self, struct: StructNode): self._struct[struct.name] = struct
    def space_def(self, space: SpaceNode): self._space[space.name] = space

    def get(self, name: str) -> BaseNode:
        try:
            if name in self._var: return self._get_var(name=name)
            elif name in self._const: return self._get_const(name=name)
            elif name in self._func: return self._get_func(name=name)
            elif name in self._struct: return self._get_struct(name=name)
            elif name in self._space: return self._get_space(name=name)
            raise NameError(f"Couldn't find '{name}' in '{self.name}' space")
        except Exception as e: Reg.get("curr_tab").write(f"[Error] {e}")

    def _get(self, name: str, attr: str, label: str):
        storage = getattr(self, attr)
        if name in storage: return storage[name]
        if self._parent is not None: return getattr(self._parent, f"_get_{label}")(name)
        raise NameError(f"Couldn't find '{name}' {label} in '{self._name}' space")

    def _get_var(self, name: str) -> ValueNode: self._get(name, "_var", "var")
    def _get_const(self, name: str) -> ValueNode: self._get(name, "_const", "const")
    def _get_func(self, name: str) -> FuncNode: self._get(name, "_func", "func")
    def _get_struct(self, name: str) -> StructNode: self._get(name, "_struct", "struct")
    def _get_space(self, name: str) -> SpaceNode: self._get(name, "_space", "space")

    def __repr__(self): return f"Environment: {self._name}"
