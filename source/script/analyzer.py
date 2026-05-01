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
            "&&", "--", "//", "||",
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

            if i + 1 < len(code):
                _dchar = code[i:i+2]
                if _dchar in self.spec_dchars:
                    for c in _dchar: 
                        self.pos.adv(c); i += 1
                    yield (_dchar, start_pos)
                    continue

            if _char in self.spec_chars:
                self.pos.adv(_char); i += 1
                yield (_char, start_pos)
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

        if   _is_dchar(value)  : return TokType.get(value,      TokType["UNKNOWN"])
        elif _is_schar(value)  : return TokType.get(value,      TokType["UNKNOWN"])
        elif _is_int(value)    : return TokType.get("INT",      TokType["UNKNOWN"])
        elif _is_float(value)  : return TokType.get("FLOAT",    TokType["UNKNOWN"])
        elif _is_str(value)    : return TokType.get("STR",      TokType["UNKNOWN"])
        elif _is_char(value)   : return TokType.get("CHAR",     TokType["UNKNOWN"])
        elif _is_bool(value)   : return TokType.get("BOOL",     TokType["UNKNOWN"])
        elif _is_block(value)  : return TokType.get("BLOCK",    TokType["UNKNOWN"])
        elif _is_loop(value)   : return TokType.get("LOOP",     TokType["UNKNOWN"])
        elif _is_kword(value)  : return TokType.get("KWORD",    TokType["UNKNOWN"])
        elif _is_func(value)   : return TokType.get("FUNC",     TokType["UNKNOWN"])
        elif _is_class(value)  : return TokType.get("CLASS",    TokType["UNKNOWN"])
        elif _is_incl(value)   : return TokType.get("INCL",     TokType["UNKNOWN"])
        elif _is_name(value)   : return TokType.get("NAME",     TokType["UNKNOWN"])
        return TokType["UNKNOWN"]

    def tokenize(self, code: str) -> list:
        tokens: list[Token] = []
        for tok in self._process_code(code):
            tok_type = self._type_check(tok[0]); tok_pos = tok[1]
            tokens.append(Token(tok_type, tok[0], tok_pos))

        return tokens

class Parser():
    def __init__(self): Reg.set("Parser", self)

    def adv(self): 
        self.idx += 1
        if self.idx < len(self.tokens): return self.tokens[self.idx]
    def curr(self): 
        if self.idx < len(self.tokens): return self.tokens[self.idx]
    def curr_check(self, _type: int) -> bool:
        return self.curr() is None or self.curr().type != _type
    def peek(self): 
        if self.idx + 1 < len(self.tokens): return self.tokens[self.idx + 1]

    def _code_process(self, tok: Token) -> BaseNode:
        if tok.type in range(1, 6):
            return self._value()

        if tok.type == TokType["NAME"]:
            try: return self._call()
            except SyntaxError as e:
                Reg.get("curr_tab").write(f"[Error] {e}")

        if tok.value == "set": 
            try: return self._var()
            except SyntaxError as e:
                Reg.get("curr_tab").write(f"[Error] {e}")

        if tok.value == "func":
            try: return self._func()
            except SyntaxError as e:
                Reg.get("curr_tab").write(f"[Error] {e}")

        if tok.value == "struct":
            pass

    def _var(self) -> AsgNode:
        self.adv()

        if self.curr_check(TokType["NAME"]):
            raise SyntaxError("Expected var name after 'set', got name for var")
        _var_name = self.curr().value
        self.adv()

        if self.curr_check(TokType["="]):
            raise SyntaxError("Expected '=' after var name, got '=' to assign value to var")
        self.adv()

        _value = self._code_process(self.curr())
        return AsgNode(_var_name, _value)

    def _value(self) -> ValueNode:
        if self.curr() is None: raise SyntaxError("Unexpected end of input while parsing value")

        tok = self.curr()
        if tok.type == TokType["INT"]:
            return ValueNode(int(tok.value))
        elif tok.type == TokType["FLOAT"]:
            return ValueNode(float(tok.value))
        elif tok.type == TokType["STR"]: # remove quotes
            return ValueNode(str(tok.value[1:-1])) 
        elif tok.type == TokType["CHAR"]: # remove quotes
            return ValueNode(str(tok.value[1:-1]))
        elif tok.type == TokType["BOOL"]:
            return ValueNode(tok.value.lower() == "true")
        else: raise SyntaxError(f"Expected a value, got {tok}")

    def _block(self) -> BlockNode:
        if self.curr_check(TokType["{"]):
            raise SyntaxError("Expected '{' to start block, got '{' to mark the start of block")
        self.adv()
        statements: list[BaseNode] = []

        while self.curr_check(TokType["}"]):
            start_idx = self.idx
            tok = self.curr()
            # print(tok) # debug code

            code = self._code_process(tok)
            statements.append(code)

        return BlockNode(statements)

    def _func(self) -> FuncNode:
        self.adv()

        if self.curr_check(TokType["NAME"]):
            raise SyntaxError("Expected func name after 'func', got name for func")
        _func_name = self.curr().value
        self.adv()

        if self.curr_check(TokType["("]):
            raise SyntaxError("Expected '(' after func name, got '(' to mark the start of func params")
        self.adv()

        _params: list[str] = []
        while self.curr().type != TokType[")"]:
            if self.curr_check(TokType["NAME"]):
                raise SyntaxError("Expected param name, got name for param")
            _params.append(self.curr().value)
            self.adv()

            if self.curr().type == TokType[","]: self.adv()
            elif self.curr_check(TokType[")"]):
                raise SyntaxError("Expected ',' or ')' in param list, got ',' of ')'")

        self.adv()

        _body = self._block()

        return FuncNode(_func_name, _params, _body)

    def _call(self) -> CallNode:
        if self.curr_check(TokType["NAME"]):
            raise SyntaxError("Expected func name after name, got name for func")
        _func_name = self.curr().value
        self.adv()

        if self.curr_check(TokType["("]):
            raise SyntaxError("Expected '(' after func name, got '(' to mark the start of func args")
        self.adv()

        _args: list[BaseNode] = []
        while self.curr_check(TokType[")"]):
            arg = self._code_process(self.curr())
            _args.append(arg)

            if self.curr().type == TokType[","]: self.adv()
            elif self.curr_check(TokType[")"]):
                raise SyntaxError("Expected ',' or ')' in arg list, got ',' or ')'")

        self.adv()
        return CallNode(_func_name, _args)

    def parse(self, tokens: list[Token]) -> list[BaseNode]:
        self.tokens = tokens
        self.idx = 0
        statements = []
        
        while self.idx < len(self.tokens):
            tok = self.curr()
            if tok is None: break
            if tok.value in (";", "\n"): self.adv(); continue
            node = self._code_process(tok)
            if node: statements.append(node)
            self.adv()
                
        return statements

def Analyze(code: str) -> list:
    Lexer(); Parser()
    tokens = Reg.get("Lexer").tokenize(code=code)
    AST_root = Reg.get("Parser").parse(tokens=tokens)

    return AST_root

if __name__ == "__main__":
    print("This is a module, not a script. Please import it to use.")
    input("Press Enter to exit...")
