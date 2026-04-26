import sys, os
import string
import re

TokType = { # vnshell type dict
    "INT"   : 0, "FLOAT" : 1,
    "STR"   : 2, "CHAR"  : 3,
    "BOOL"  : 4,

    "NAME"  : 5, "KWORD" : 6,
    "BLOCK" : 7, "LOOP"  : 8,
    "CALL"  : 9, 

    "("     : 48, ")"     : 49,
    "["     : 50, "]"     : 51,
    "{"     : 52, "}"     : 53,
    "<"     : 54, ">"     : 55,

    "!"     : 56, "@"     : 57,
    "#"     : 58, "$"     : 59,
    "%"     : 60, "^"     : 61,
    "&"     : 62, "*"     : 63,
    "-"     : 64, "+"     : 65,
    "="     : 66,

    ":"     : 67, ";"     : 68,
    "\'"    : 69, "\""    : 70,
    "/"     : 71, "\\"    : 72,
    ","     : 73, "."     : 74,
    "?"     : 75, "|"     : 76,

    "UNKNOWN": 255
}

TokType_ID = { # type dict, but had been reversed
    0: "INT", 1: "FLOAT", 2: "STR", 3: "CHAR", 4: "BOOL",
    5: "NAME", 6: "KWORD", 7: "BLOCK", 8: "LOOP", 9: "CALL",

    48: "O1"    , 49: "C1",
    50: "O2"    , 51: "C2",
    52: "O3"    , 53: "C3",
    54: "O4"    , 55: "C4",

    56: "NOT",   57: "AT",
    58: "HASH",   59: "DOL",
    60: "MOD",    61: "POW",
    62: "AND",    63: "MUL",
    64: "SUB",    65: "ADD",
    66: "ASG",

    67: "COLON",  68: "SEMI",
    69: "SQ",     70: "DQ",
    71: "DIV",    72: "PATH",
    73: "COMMA",  74: "DOT",
    75: "QUEST",  76: "PIPE",

    255: "UNKNOWN"
}

class Token():
    def __init__(self, value: str, type: int):
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return f"Token:value {self.value} | type {TokType_ID[self.type]}"

if __name__ == "__main__":
    print("[info] This file only import")
    input("Press Enter to exit...")
