
# --- func ---

# system modules
import os, sys

# registry
from source.registry import Reg

# app module
from source.script.analyzer.lexer import Lexer
from source.script.analyzer.parser import Parser

def analyzer_setup() -> None:
    Lexer(); Parser()

def analyze(code: str) -> list:
    tokens = Reg.get("Lexer").tokenize(code)
    print(tokens) # debug code
    Ast = Reg.get("Parser").parse(tokens)

    return Ast

# ------------
