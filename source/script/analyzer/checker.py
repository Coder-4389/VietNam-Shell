# system modules
import sys, os

# app modules
from source.script.node import *
from source.script.token import *
from source.script.typedef import *

class VBaseErr(BaseException):
    def __init__(self,
        _type: str=None,
        _info: str=None,
    ):
        super().__init__()
        self.err_type = _type
        self.err_info = _info

    def __str__(self):
        return f"[Error] {self.err_type}: {self.err_info}"

class VNameErr(VBaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("NameError", _info)

class VSyntaxErr(VBaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("SyntaxError", _info)

class VTypeErr(VBaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("TypeError", _info)

class VUnknownErr(VBaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("UnknownError", _info)
