TokType = {
    # --- Data (0 - 9) ---
    "NAME"     : 0, 
    "INT"      : 1, 
    "FLOAT"    : 2, 
    "STR"      : 3,
    "CHAR"     : 4,
    "BOOL"     : 5,

    # --- Keywords (10 - 29) ---
    "BLOCK"    : 10,                          # if, elif, else 
    "LOOP"     : 11,                          # for, while 
    "FUNC"     : 12,                          # function
    "CLASS"    : 13,                          # class
    "KWORD"    : 14,                          # keyword
    "INCL"     : 15,                          # include

    # --- Symbols (30 - 69) ---
    "{"        : 32, "}"  : 33,               # { } 
    "["        : 34, "]"  : 35,               # [ ]  
    "("        : 36, ")"  : 37,               # ( ) 
    ","        : 38,                          # , 
    "."        : 39,                          # . 
    ";"        : 40,                          # ; 
    ":"        : 41,                          # : 
    "?"        : 42,                          # ? 
    "@"        : 43,                          # @ 
    "#"        : 44,                          # # 
    "$"        : 45,                          # $ 
    "&"        : 46,                          # & 
    "|"        : 47,                          # | 
    
    "+"        : 48, "-" : 49, "*" : 50, "/" : 51, "%" : 52, # + - * / % 
    "="        : 53,                          # : 
    "!"        : 54,                          # ! 
    "\""       : 55,                          # ' 
    "\'"       : 56,                          # " 

    "UNKNOWN"  : 255,
}

TokName = {
    # --- Data ---
    0: "NAME", 1: "INT", 2: "FLOAT", 3: "STR", 4: "CHAR", 5: "BOOL",

    # --- Keywords ---
    10: "BLOCK",    11: "LOOP",
    12: "FUNC",     13: "CLASS",
    14: "KWORD",    15: "INCL",

    # --- Symbols ---
    32: "L3",       33: "R3",
    34: "L2",       35: "R2",
    36: "L1",       37: "R1",
    38: "Comma",    39: "Dot",
    40: "Semi",     41: "Colon",
    42: "Quest",    43: "At",
    44: "Hash",     45: "Dol",
    46: "Amp",      47: "Pipe",
    48: "Add",      49: "Sub",
    50: "Mul",      51: "Div",
    52: "Mod",      53: "Asg",
    54: "Not", 
    55: "SQ",       56: "DQ",

    255: "UNKNOWN"
}

class Pos():
    def __init__(self,
        line: int=0,
        col: int=0,
        idx: int=0
    ): 
        self.line = line
        self.col = col
        self.idx = idx

    def adv(self, curr_char: str="") -> None:
        self.idx += 1; self.col += 1
        if curr_char == "\n": 
            self.line += 1; self.col = 0

    def copy(self): 
        return Pos(
            self.line, 
            self.col, 
            self.idx
        )

class Token():
    def __init__(self,
        _type: int=255,
        value: str="",
        pos: Pos=Pos()
    ): 
        self.type = _type
        self.value = value

        self.pos = pos

    def __str__(self) -> str:
        return f"{TokName.get(self.type, 'UNKNOWN')}({self.value}) at {self.pos.line}:{self.pos.col}"

    def __repr__(self) -> str:
        return f"{TokName.get(self.type, 'UNKNOWN')}({self.value}) at {self.pos.line}:{self.pos.col}"