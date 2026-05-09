# system modules
import sys, os

# Registry
from source.registry import Reg

# script modules
from source.script.node import *
from source.script.token import *
from source.script.typedef import *
from source.script.analyzer.envdef import Environment


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
    def in_env(self, name: str="") -> None:
        _env = Environment(_name=name, parent=self.curr_env)
        self._envs.append(_env) 
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
        if not self.curr: raise SyntaxError("Expected expression")
        tok = self.curr
        if tok.value in ("not", "-", "+"):
            self.adv()
            return OpNode(op=tok.value, left=None, right=self._value())

        if tok.value == "(":
            self.adv()
            node = self._expr()
            if not self.curr or self.curr.value != ")":
                raise SyntaxError("Missing closing parenthesis ')'")
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
            converter, _type = value_map[tok.type]
            self.adv() 
            return ValueNode(value=converter(tok.value), _type=_type)

        if self.match(Tok_t["NAME"]):
            node = self._use(tok) 
            self.adv()
            return node

        raise SyntaxError(f"Unexpected token: {tok.value}")

    def _cond(self) -> BaseNode: 
        cond_node = self._expr(mopl=-3)
        if self.curr and self.curr.value == "{": return cond_node
        raise SyntaxError("Missing '{' after condition")

    def _block(self) -> BaseNode: 
        if not self.match(Tok_t["{"]):
            raise SyntaxError("Missing '{' before block")
        self.adv()
        
        statements: list[BaseNode] = list()

        while self.idx < len(self.tokens) and not self.match(Tok_t["}"]):
            if self.curr.value in [';', '\n']:
                self.adv()
                continue

            tok = self.curr
            try:
                if self.match(Tok_t["NAME"]): 
                    node = self._use(tok)
                else: node = self._define(tok)
                if node: statements.append(node)
            except Exception as e:
                Reg.get("curr_tab").write(f"[Block Error] {e}")
                self.adv()

        if not self.match(Tok_t["}"]):
            raise SyntaxError("Missing '}' after block")
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

    def _loop(self) -> BaseNode: 
        if self.curr.value == "while": _mode = "while"
        elif self.curr.value == "for": _mode = "for"

        self.adv()

    def _asg(self) -> BaseNode:
        if self.curr.value == "set": _mode = "set"
        elif self.curr.value == "const": _mode = "const"

        self.adv()
        if self.curr.type != Tok_t["NAME"]:
            raise SyntaxError(f"Expected var name to assign the var")
        _name = self.curr.value
        self.adv()
        
        valid_ops = ["=", "+=", "-=", "*=", "/=", "%="]
        if self.curr.value not in valid_ops:
            raise SyntaxError(f"Expected '=' to assign the var")
        self.adv()

        tok = self.curr
        _value = self._expr()

        if _mode == "set": self.curr_env.var_def(name=_name, _type=_value.type)
        elif _mode == "const": self.curr_env.const_def(name=_name, _type=_value.type)
        return AsgNode(name=_name, value=_value)

    def _func(self) -> BaseNode: 
        self.adv()

        if not self.match(Tok_t["NAME"]):
            raise SyntaxError("Expected function name")
        _name = self.curr.value
        self.adv()

        if not self.match(Tok_t["("]):
            raise SyntaxError("Expected '(' after function name")
        self.adv()

        params: list[str] = []

        while self.idx < len(self.tokens) and not self.match(Tok_t[")"]):
            if not self.match(Tok_t["NAME"]):
                raise SyntaxError("Expected parameter name")
            _param_name = self.curr.value
            params.append(_param_name)
            self.adv()

            if self.match(Tok_t[","]): self.adv()
            else: break

        if not self.match(Tok_t[")"]):
            raise SyntaxError("Expected ')' after parameters")
        self.adv()

        _body = self._block()

        self.curr_env.func_def(FuncNode(name=_name, params=params, body=_body))
        return FuncNode(name=_name, params=params, body=_body)

    def _struct(self) -> BaseNode: 
        self.adv()

        if not self.match(Tok_t["NAME"]):
            raise SyntaxError("Expected struct name")
        _name = self.curr.value
        self.adv()

        if not self.match(Tok_t["{"]):
            raise SyntaxError("Expected '{' after struct name")
        self.adv()

        members: dict[str, Vtype]= dict()

        while self.idx < len(self.tokens) and not self.match(Tok_t["}"]):
            if self.curr.value in [';', '\n']:
                self.adv(); continue

            if not self.match(Tok_t["NAME"]):
                raise SyntaxError("Expected member name")
            _name_member = self.curr.value
            self.adv()

            if not self.match(Tok_t[":"]):
                raise SyntaxError("Expected ':' after member name")
            self.adv()

            _type_member = self.curr.value

            if _type_member not in Vts:
                raise SyntaxError(f"Unknown type '{_type_member}'")
            self.adv()

            members[_name_member] = Vts[_type_member]

            if self.match(Tok_t[","]): 
                self.adv()

        return StructNode(name=_name, list_item=members)

    def _space(self) -> BaseNode: ...


    def _use(self, tok: Token) -> BaseNode: 
        if self.peek().type == Tok_t["("]: return self._call()
        elif self.peek().type == Tok_t["."]: return self._access()
        else: return self._var()
        raise SyntaxError(f"Unexpected token: {tok.value}")

    def _call(self): ...
    def _access(self): ...
    def _var(self): ...

    # ---------------

    def parse(self, tokens: list[Token]) -> list[BaseNode]:
        self.tokens = tokens
        self.idx = 0

        self._envs: list[Environment] = [Environment(_name="global")]
        ast: list[BaseNode] = []

        while self.idx < len(self.tokens):
            if self.curr.value in [";", "\n"]:
                self.adv()
                continue

            # start_tok = self.curr 
            # if self.match(Tok_t["NAME"]): node = self._use(start_tok)
            # else: node = self._define(start_tok)
            # if node: ast.append(node)
            # debug code

            try:
                start_tok = self.curr 
                if self.match(Tok_t["NAME"]): node = self._use(start_tok)
                else: node = self._define(start_tok)
                if node: ast.append(node)
            except Exception as e:
                line = getattr(start_tok.pos, 'line', '?')
                col = getattr(start_tok.pos, 'col', '?')
                Reg.get("curr_tab").write(f"[Error at {line}:{col}] {e}")
                if self.idx < len(self.tokens): self.adv()
                else: break

        return ast
