# process modules
import string
import json

# system modules
import sys, os

# Registry
from source.registry import Reg

# App modules
from source.script.token import *
from source.script.node import *
from source.script.typedef import *

def _kword_load() -> list[str]:
    listed_keywords: list[str] = []
    for group in Reg.get("keywords").values():
        for kw in group: listed_keywords.append(kw)

    return listed_keywords

class Lexer:
    def __init__(self) -> list:
        self.spec_chars = set(string.punctuation) - {"_"}
        self.spec_dchars = {
            "==", "!=", "|=", ">=", "<=", "%=", "*=", "/=", "+=", "-=",
        }; self.pos = Pos()

        Reg.set("Lexer", self)

    def _process_code(self, code: str) -> tuple:
        i: int = 0

        while i < len(code):
            _char = code[i]
            start_pos = self.pos.copy()

            if _char.isspace():
                self.pos.adv(_char); i += 1
                continue

            if _char == '"':
                start = i
                self.pos.adv(code[i]); i += 1
                while i < len(code) and code[i] != '"':
                    self.pos.adv(code[i]); i += 1
                if i < len(code):
                    self.pos.adv(code[i]); i += 1
                yield (code[start:i], start_pos)
                continue

            if _char.isalnum() or _char == '_':
                start = i
                while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                    self.pos.adv(code[i]); i += 1
                yield (code[start:i], start_pos)
                continue

            if i + 1 < len(code):
                _dchar = code[i:i+2]
                if _dchar in self.spec_dchars:
                    for c in _dchar: self.pos.adv(c); i += 1
                    yield (_dchar, start_pos)
                    continue

            if _char in self.spec_chars:
                self.pos.adv(_char); i += 1
                yield (_char, start_pos)
                continue
                
            self.pos.adv(_char); i += 1
            yield (_char, start_pos)

    def _type_check(self, value: str) -> str: 
        _is_int     = lambda v: v.isdigit()
        _is_float   = lambda v: len(v) > 1 and v.replace('.', '', 1).isdigit()
        _is_str     = lambda v: v.startswith('"') and v.endswith('"')
        _is_char    = lambda v: v.startswith("'") and v.endswith("'")
        _is_bool    = lambda v: v.lower() in ['true', 'false']
        _is_name    = lambda v: v.isidentifier()
        _is_kword   = lambda v: v in _kword_load()
        _is_block   = lambda v: v in ["if", "elif", "else"]
        _is_loop    = lambda v: v in ["for", "while"]
        _is_schar   = lambda v: v in self.spec_chars
        _is_dchar   = lambda v: v in self.spec_dchars
        _is_func    = lambda v: v == "func"
        _is_class   = lambda v: v == "class"
        _is_incl    = lambda v: v == "include"

        if   _is_dchar(value)  : 
            return Tok_t.get(value, Tok_t["UNKNOWN"])
        elif _is_schar(value)  : 
            return Tok_t.get(value, Tok_t["UNKNOWN"])
        elif _is_int(value)    : 
            return Tok_t.get("INT", Tok_t["UNKNOWN"])
        elif _is_float(value)  : 
            return Tok_t.get("FLOAT", Tok_t["UNKNOWN"])
        elif _is_str(value)    : 
            return Tok_t.get("STR", Tok_t["UNKNOWN"])
        elif _is_char(value)   : 
            return Tok_t.get("CHAR", Tok_t["UNKNOWN"])
        elif _is_bool(value)   : 
            return Tok_t.get("BOOL", Tok_t["UNKNOWN"])
        elif _is_block(value)  : 
            return Tok_t.get("BLOCK", Tok_t["UNKNOWN"])
        elif _is_loop(value)   : 
            return Tok_t.get("LOOP", Tok_t["UNKNOWN"])
        elif _is_kword(value)  : 
            return Tok_t.get("KWORD", Tok_t["UNKNOWN"])
        elif _is_func(value)   : 
            return Tok_t.get("FUNC", Tok_t["UNKNOWN"])
        elif _is_class(value)  : 
            return Tok_t.get("CLASS", Tok_t["UNKNOWN"])
        elif _is_incl(value)   : 
            return Tok_t.get("INCL", Tok_t["UNKNOWN"])
        elif _is_name(value)   : 
            return Tok_t.get("NAME", Tok_t["UNKNOWN"])
        return Tok_t["UNKNOWN"]

    def tokenize(self, code: str) -> list:
        tokens: list[Token] = []
        for tok in self._process_code(code):
            tok_type = self._type_check(tok[0]); tok_pos = tok[1]
            tokens.append(Token(tok_type, tok[0], tok_pos))

        return tokens

class Space():
    def __init__(self, _name: str="", parent: "SpaceEnv"=None):
        self._name = _name
        self._parent = parent

        self._var: dict[str, ValueNode] = dict()
        self._const: dict[str, ValueNode] = dict()

        self._func: dict[str, FuncNode] = dict()
        self._struct: dict[str, StructNode] = dict()
        self._space: dict[str, SpaceNode] = dict()

    def var_def(self, name: str, value: Vts): 
        if name in self._const: raise SyntaxError(f"Var '{name}' is already defined as a const.")
        self._var[name] = value
    def const_def(self, name: str, value: Vts): 
        if name in self._var: raise SyntaxError(f"Const '{name}' is already defined as a var.")
        self._const[name] = value
    def func_def(self, func: FuncNode): 
        self._func[func.name] = func
    def struct_def(self, struct: StructNode): 
        self._struct[struct.name] = struct
    def space_def(self, space: SpaceNode): 
        self._space[space.name] = space

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

    def __repr__(self): return f"Space: {self._name}"

class Parser():
    def __init__(self): Reg.set("Parser", self)

    # --- tok ---
    @property
    def curr(self): return self.tokens[self.idx]
    def adv(self, cnt: int=1) -> None: self.idx += cnt
    def peek(self, cnt: int=0): return self.tokens[self.idx + cnt]

    def match(self, _type: int=255) -> bool: return self.curr and self.curr.type == _type
    # -----------

    # --- env ---
    @property
    def curr_env(self): return self._envs[-1]
    def mk_env(self, name: str="") -> None:
        self.curr_env._space[name] = _env
        _env = Space(_name=name, parent=self.curr_env)
        self._envs.append(_env) 
    def del_env(self) -> None: 
        if len(self._envs) > 1: self._envs.pop()
    # -----------

    # --- process ---
    def _process(self, tok: Token):
        if tok.type == Tok_t["NAME"]:
            try: 
                if self.peek().type == Tok_t["("]: return self._call()
                elif self.peek().type == Tok_t["."]: return self._access()
                else: return self._var()
            except Exception as e: Reg.get("curr_tab").write(f"[Error] {e}")

        if tok.value in ["set", "const"]:
            try: return self._asg()
            except Exception as e: Reg.get("curr_tab").write(f"[Error] {e}")

    def _asg(self) -> BaseNode:
        if self.curr.value == "set": _mode = "set"
        elif self.curr.value == "const": _mode = "const"

        self.adv()
        if self.curr.type != Tok_t["NAME"]:
            raise SyntaxError(f"Expected var name to assign the var")
        _name = self.curr.value
        self.adv()
        
        valid_ops = ["=", "+=", "-=", "*=", "/=", "%="]
        if self.curr.type in valid_ops:
            raise SyntaxError(f"Expected '=' to assign the var")
        self.adv()

        tok = self.curr
        _value = self._process(tok)

        return AsgNode(name=_name, value=_value)

    def _func(self) -> BaseNode: ...
    def _struct(self) -> BaseNode: ...
    def _space(self) -> BaseNode: ...
    def _if(self) -> BaseNode: ...
    def _loop(self) -> BaseNode: ...

    def _call(self): ...
    def _access(self): ...
    def _var(self): ...
    # ---------------

    def parse(self, tokens: list[Token]) -> Space:
        self.tokens = tokens; self.idx = -1

        self._envs: list[Space] = [Space(_name="global")]

        while self.idx < len(self.tokens) - 1:
            tok = self.curr
            if tok.value in [';', '\n']:
                self.adv(); continue

            code = self._process(tok)
            

def analyze(code: str) -> list:
    pass

if __name__ == "__main__":
    print("This is a module, not a script. Please import it to use.")
    input("Press Enter to exit...")
