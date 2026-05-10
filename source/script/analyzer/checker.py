# system modules
import sys, os

# app modules
from source.script.node import *
from source.script.token import *
from source.script.typedef import *

class BaseErr(BaseException):
    def __init__(self,
        _type: str=None,
        _info: str=None,
    ):
        super().__init__()
        self.err_type = _type
        self.err_info = _info

    def __str__(self):
        return f"[Error] {self.err_type}: {self.err_info}"

class NameErr(BaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("NameError", _info)

class SyntaxErr(BaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("SyntaxError", _info)

class TypeErr(BaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("TypeError", _info)

class UnknowErr(BaseErr):
    def __init__(self, _info: str=None): 
        super().__init__("UnknownError", _info)
