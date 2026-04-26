import sys, os
import string
import re

from .token import *

KeyWord = { # vnshell keyword 
    # actions:
    "say", # print content like echo command

    # modifity:
    "ngan", # run cmd with admin perms
}

class _Lexer():
    def __init__(self, code: str):
        self.cmd = code
        self.tokens = []
        self.size = 0

        self._tokenize()

    def _char_process(self) -> str:
        spec_char = set(string.punctuation) - {'_'} # special charater set 
        print(spec_char)
        for char in spec_char: self.cmd = self.cmd.replace(char, f" {char} ")
        return self.cmd

    def _tok_process(self) -> list:
        self._char_process()
        dirty_toks = self.cmd.strip().split()
        clean_toks = []
        for tok in dirty_toks:
            if tok: clean_toks.append(tok)
            self.size += 1
        return clean_toks

    def _type_process(self, value: str) -> int:
        _is_int     = lambda self, v: v.isdigit()
        _is_float   = lambda self, v: len(v) > 1 and v.replace('.', '', 1).isdigit()
        _is_str     = lambda self, v: v.startswith('"') and v.endswith('"')
        _is_char    = lambda self, v: v.startswith("'") and v.endswith("'")
        _is_bool    = lambda self, v: v.lower() in ['true', 'false']
        _is_name    = lambda self, v: v.isidentifier()
        _is_kword   = lambda self, v: v in KeyWord
        _is_block   = lambda self, v: v in ["if", "elif", "else"]
        _is_loop    = lambda self, v: v in ["for", "while"]
        _is_schar   = lambda self, v: (
            len(v) == 1 and 
            v in set(string.punctuation)-{'_'}
        )

        if   _is_int(value)    : return TokType.get("INT", TokType["UNKNOWN"])
        elif _is_float(value)  : return TokType.get("FLOAT", TokType["UNKNOWN"])
        elif _is_str(value)    : return TokType.get("STR", TokType["UNKNOWN"])
        elif _is_char(value)   : return TokType.get("CHAR", TokType["UNKNOWN"])
        elif _is_bool(value)   : return TokType.get("BOOL", TokType["UNKNOWN"])
        elif _is_schar(value)  : return TokType.get(value, TokType["UNKNOWN"])
        elif _is_block(value)  : return TokType.get("BLOCK", TokType["UNKNOWN"])
        elif _is_loop(value)   : return TokType.get("LOOP", TokType["UNKNOWN"])
        elif _is_kword(value)  : return TokType.get("KWORD", TokType["UNKNOWN"])
        elif _is_name(value)   : return TokType.get("NAME", TokType["UNKNOWN"])
        return TokType["UNKNOWN"]

    def _tokenize(self):
        for tok in self._tok_process():
            token = Token(tok, self._type_process(tok))
            self.tokens.append(token)
            # print(token)

class _Parser():
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.tok_ptr = 0

    def _resume(self, _type: int=255):
        if _type != 255 and self.tokens[self.ptr].type == _type: self.tok_ptr += 1
        elif _type == 255: self.tok_ptr += 1
        else: return f"[Error] The codes have a error"

if __name__ == "__main__":
    print("[info] This file only import")
    input("Press Enter to exit...")