# system modules
import sys, os

# Registry
from source.registry import Reg

# script modules
from source.script.node import *
from source.script.token import *
from source.script.typedef import *

# analyzer modules
from source.script.analyzer.context import *

class Parser():
    def __init__(self): Reg.set("Parser", self)
    
    def __call__(self, tokens: list[Token]) -> list[BaseNode]:
        self.tokens = tokens
        self.idx = 0

        self._envs: list[Environment] = [Environment(_name="global")]
        ast: list[BaseNode] = []

        while self.idx < len(self.tokens):
            if self.match(Tok_t[";"]):
                self.adv(); continue

            # start_tok = self.curr 
            # if self.match(Tok_t["NAME"]): node = self._use(start_tok)
            # else: node = self._define(start_tok)
            # if node: ast.append(node)
            # # debug code

            try:
                start_tok = self.curr 
                if self.match(Tok_t["NAME"]): node = self._ref(start_tok)
                else: node = self._define(start_tok)
                if node: ast.append(node)
            except BaseErr as e: Reg.get("curr_tab").write(e); break
            except KeyboardInterrupt: sys.exit(0)

        return ast

    # --- tok ---
    @property
    def curr(self) -> Token: 
        try: return self.tokens[self.idx]
        except: return Token()
    def adv(self, cnt: int=1) -> None: self.idx += cnt
    def peek(self, cnt: int=0): return self.tokens[self.idx + cnt]

    def match(self, _type: int=255) -> bool: return self.curr and self.curr.type == _type
    # -----------

    # --- env ---
    @property
    def curr_env(self): return self._envs[-1]
    def in_env(self, name: str="") -> None:
        _env = Environment(_name=name, parent=self.curr_env)
        self._envs.append(_env)
    def cl_env(self) -> None: self._envs.append(self.curr_env)
    def out_env(self) -> None: 
        if len(self._envs) > 1: self._envs.pop()
    # -----------

    # --- process ---
    def _define(self, tok: Token):
        if tok.value in ["set", "const"]: return self._asg()
        if tok.value in ["func"]: return self._func()
        if tok.value in ["struct"]: return self._struct()
        if tok.value in ["space"]: return self._space()
        if tok.value in ["if", "elif", "else"]: return self._if()
        if tok.value in ["while", "for"]: return self._loop()

        return self._expr()

    def _expr(self, mopl: int=-3) -> BaseNode: 
        ops_level = {
            '+': 0, '-': 0,
            '*': 1, '/': 1,
            '%': 1, '//': 1,
            '^': 2, 

            '==' : -1, '!=': -1,
            '>'  : -1, '>=': -1,
            '<'  : -1, '<=': -1,
            'and': -2, 'or': -3,
        }

        left_val = self._value()

        while self.idx < len(self.tokens):
            if not self.curr or self.curr.value not in ops_level: 
                break

            opl = ops_level[self.curr.value]
            if opl < mopl: break

            op = self.curr.value
            self.adv()
            opl = opl if op == '^' else opl + 1
            right_val = self._expr(mopl=opl) 
            left_val = OpNode(op=op, left=left_val, right=right_val)
        
        return left_val

    def _value(self) -> BaseNode:
        if not self.curr: raise SyntaxErr("Expected expression")
        tok = self.curr
        if tok.value in ("not", "-", "+"):
            self.adv()
            return OpNode(op=tok.value, left=None, right=self._value())

        if tok.value == "(":
            self.adv()
            node = self._expr()
            if not self.curr or self.curr.value != ")": raise SyntaxErr("Missing closing parenthesis ')'")
            self.adv()
            return node

        value_map = {
            Tok_t["INT"]:   (int, BaseTypes["INT"]),
            Tok_t["FLOAT"]: (float, BaseTypes["FLOAT"]),
            Tok_t["STR"]:   (lambda v: v[1:-1], BaseTypes["STR"]),
            Tok_t["CHAR"]:  (lambda v: v[1], BaseTypes["CHAR"]),
            Tok_t["BOOL"]:  (lambda v: v.lower() == "true", BaseTypes["BOOL"]),
        }

        if tok.type in value_map:
            converter, _type = value_map[tok.type]; self.adv() 
            return ValueNode(value=converter(tok.value), _type=_type)

        if self.match(Tok_t["NAME"]):
            node = self._ref(tok); self.adv()
            return node

        raise VunknownErr(f"Unexpected token: {tok.value}")

    def _cond(self) -> BaseNode: 
        cond_node = self._expr(mopl=-3)
        if self.curr and self.curr.value == "{": return cond_node
        raise SyntaxErr("Missing '{' after condition")

    def _block(self, in_func: bool=False) -> BaseNode: 
        if not self.match(Tok_t["{"]): raise SyntaxErr("Missing '{' before block")
        self.adv()
        
        statements: list[BaseNode] = list()

        while self.idx < len(self.tokens) and not self.match(Tok_t["}"]):
            if self.curr.value in [';', '\n']:
                self.adv(); continue

            tok = self.curr
            try:
                if self.match(Tok_t["NAME"]): node = self._ref(tok)
                elif self.curr.value == "return" and in_func: node = self._return()
                else: node = self._define(tok)
                if node: statements.append(node)
            except BaseErr as e:
                Reg.get("curr_tab").write(f"[Block Error] {e}")
                self.adv()

        if not self.match(Tok_t["}"]): raise SyntaxErr("Missing '}' after block")
        self.adv() 

        return BlockNode(statements=statements)

    def _if(self) -> BaseNode: 
        self.adv()
        _cond = self._cond()
        _body = self._block()

        _el = None

        if not self.curr: # return when don't have elif, else
            return IfNode(condition=_cond, true_block=_body)

        if self.curr.value == "elif":
            _el = self._if()
        elif self.curr.value == "else":
            self.adv()
            _el = self._block()

        return IfNode(condition=_cond, true_block=_body, false_block=_el)

    def _return(self) -> BaseNode:
        self.adv()
        
        if self.curr and self.curr.value in (';', '\n', '}'): 
            return ReturnNode(value=None)
        _val = self._expr() 
        return ReturnNode(value=_val)

    def _loop(self) -> BaseNode: 
        _mode = self.curr.value
        self.adv()

        if _mode == "while":
            _condition = self._cond() 
            _body = self._block() 
            
            return LoopNode(mode="while", condition=_condition, body=_body)
            
        elif _mode == "for":
            if not self.match(Tok_t["NAME"]): raise SyntaxErr("Cần tên biến chạy sau 'for'")
            _var_name = self.curr.value
            self.adv()

            if self.curr.value != "in": raise SyntaxErr("Cần từ khóa 'in' sau tên biến")
            self.adv()

            _object = self._expr() 
            _body = self._block(in_func=False)

            return LoopNode(mode="for", var_name=_var_name, iterable=_object, body=_body)

    def _asg(self) -> BaseNode:
        if self.curr.value == "set": _mode = "set"
        elif self.curr.value == "const": _mode = "const"

        self.adv()
        if self.curr.type != Tok_t["NAME"]: raise SyntaxErr(f"Expected var name to assign the var")
        _name = self.curr.value
        self.adv()
        
        valid_ops = ["=", "+=", "-=", "*=", "/=", "%="]
        if self.curr.value not in valid_ops: raise SyntaxErr(f"Expected '=' to assign the var")
        self.adv()

        tok = self.curr
        _value = self._expr()

        if _mode == "set": self.curr_env.var_def(name=_name, _type=_value.type)
        elif _mode == "const": self.curr_env.const_def(name=_name, _type=_value.type)
        return AsgNode(name=_name, value=_value)

    def _func(self) -> BaseNode: 
        self.adv()

        if not self.match(Tok_t["NAME"]): raise SyntaxErr("Expected function name")
        _name = self.curr.value
        self.adv()

        if not self.match(Tok_t["("]): raise SyntaxErr("Expected '(' after function name")
        self.adv()

        _node = FuncNode(name=_name, params=[], body=None)
        self.curr_env.func_def(_node)

        params: list[str] = []
        self.in_env(name=_name)

        while self.idx < len(self.tokens) and not self.match(Tok_t[")"]):
            if not self.match(Tok_t["NAME"]): raise SyntaxErr("Expected parameter name")
            _param_name = self.curr.value
            params.append(_param_name)
            self.adv()

            if self.match(Tok_t[","]): 
                self.adv()

            self.curr_env.var_def(name=_param_name, _type=Vtype(kind=Base_ts, name="NONE"))

        if not self.match(Tok_t[")"]): raise SyntaxErr("Expected ')' after parameters")
        self.adv()

        _node.body = self._block(in_func=True)
        _node.params = params

        self.out_env()
        return _node

    def _struct(self) -> BaseNode: 
        self.adv()

        if not self.match(Tok_t["NAME"]): raise SyntaxErr("Expected struct name")
        _name = self.curr.value
        self.adv()

        if not self.match(Tok_t["{"]): raise SyntaxErr("Expected '{' after struct name")
        self.adv()

        members: dict[str, Vtype]= dict()

        while self.idx < len(self.tokens) and not self.match(Tok_t["}"]):
            if self.curr.value in [';', '\n']:
                self.adv(); continue

            if not self.match(Tok_t["NAME"]): raise SyntaxErr("Expected member name")
            _name_member = self.curr.value
            self.adv()

            if not self.match(Tok_t[":"]): raise SyntaxErr("Expected ':' after member name")
            self.adv()

            if self.curr.value not in Vts: raise SyntaxErr(f"Unknown type '{_type_member}'")
            _type_member = self.curr.value
            self.adv()

            members[_name_member] = vts[_type_member]

            if self.match(Tok_t[","]): 
                self.adv()

        if not self.match(Tok_t["}"]): raise SyntaxErr("Expected '}' after members")
        self.adv()

        self.curr_env.struct_def(StructNode(name=_name, list_item=members))
        return StructNode(name=_name, list_item=members)

    def _space(self) -> BaseNode: 
        self.adv()

        if not self.match(Tok_t["NAME"]): raise SyntaxErr("Expected space name")
        _name = self.curr.value
        self.adv()

        self.in_env(name=_name)
        _body = self._block()
        self.out_env()

        self.curr_env.space_def(SpaceNode(name=_name, statements=_body))
        return SpaceNode(name=_name, statements=_body)

    def _use(self) -> BaseNode:
        self.adv()

        if not self.match(Tok_t["NAME"]): raise SyntaxErr("Expected use name")
        _name = self.curr.value
        self.adv()

        if self.curr.value == "as":
            self.adv()
            if not self.match(Tok_t["NAME"]): raise SyntaxErr("Expected use name")
            _name = self.curr.value
            self.adv()

        _node = SpaceNode(name=_name, statements=None)
        self.curr_env.space_def(_node)
        return _node

    def _ref(self, tok: Token) -> BaseNode: 
        if self.peek().type == Tok_t["("]: return self._call()
        elif self.peek().type == Tok_t["."]: return self._access()
        else: return self._var()
        raise UnknowErr(f"Unexpected token: {tok.value}")

    def _call(self): ...
    def _access(self): ...
    def _var(self): ...

    # ---------------

