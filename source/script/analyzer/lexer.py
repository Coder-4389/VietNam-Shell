# system modules
import sys, os
import string

# Registry
from source.registry import Reg

# script modules
from source.script.node import *
from source.script.token import *
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
        _is_incl    = lambda v: v == "use"

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
            return Tok_t.get("USE", Tok_t["UNKNOWN"])
        elif _is_name(value)   : 
            return Tok_t.get("NAME", Tok_t["UNKNOWN"])
        return Tok_t["UNKNOWN"]

    def tokenize(self, code: str) -> list:
        tokens: list[Token] = []
        for tok in self._process_code(code):
            tok_type = self._type_check(tok[0]); tok_pos = tok[1]
            tokens.append(Token(tok_type, tok[0], tok_pos))

        return tokens
