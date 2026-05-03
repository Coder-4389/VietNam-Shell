# process modules
import string
import json 

# system modules
import sys, os

# Registry
# from source.registry import Reg

class BaseNode(): 
    def __repr__(self): ...

class ValueNode(BaseNode):
    def __init__(self, value: any=None): 
        self.value = value
    def __repr__(self): 
        return f"Value: {self.value}"

class ListNode(BaseNode):
    def __init__(self, elements: list[BaseNode]=[]):
        self.elements = elements
    def __repr__(self): 
        return f"List: [{', '.join(map(str, self.elements))}]"

class MapNode(BaseNode):
    def __init__(self, pairs: dict[str, BaseNode]={}):
        self.pairs = pairs
    def __repr__(self): 
        return f"Map: {{{', '.join(f'{k}: {v}' for k, v in self.pairs.items())}}}"

class AsgNode(BaseNode):
    def __init__(self, name: str="", value: BaseNode=None):
        self.name = name
        self.value = value
    def __repr__(self): 
        return f"Assign: {self.name} = {self.value}"

class OpNode(BaseNode):
    def __init__(self, op: str="", left: BaseNode=None, right: BaseNode=None):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self): 
        return f"Op: {self.left} {self.op} {self.right}"

class CallNode(BaseNode):
    def __init__(self, name: str="", args: list[BaseNode]=[]):
        self.name = name
        self.args = args
    def __repr__(self): 
        return f"Call: {self.name}({', '.join(map(str, self.args))})"

class VarNode(BaseNode):
    def __init__(self, name: str=""):
        self.name = name
    def __repr__(self): 
        return f"Var: {self.name}"

class BlockNode(BaseNode):
    def __init__(self, statements: list[BaseNode]=[]):
        self.statements = statements
    def __repr__(self): 
        return "Block: {\n" + "\n  ".join(map(str, self.statements)) + "\n}"

class FuncNode(BaseNode):
    def __init__(self, name: str="", params: list[str]=[], body: BlockNode=None):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self): 
        return f"Func: {self.name}({', '.join(self.params)}) {self.body}"

class ReturnNode(BaseNode):
    def __init__(self, value: BaseNode = None):
        self.value = value
    def __repr__(self): 
        return f"Return: {self.value}"

class CondNode(BaseNode):
    def __init__(self, left: BaseNode, op: str, right: BaseNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"Condition: ({self.left} {self.op} {self.right})"

class IfNode(BaseNode):
    def __init__(self, condition: BaseNode=None, true_block: BlockNode=None, false_block: BlockNode=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
    def __repr__(self): 
        return f"If: if ({self.condition}) {self.true_block} else {self.false_block}"

class LoopNode(BaseNode):
    def __init__(self, condition: BaseNode=None, body: BlockNode=None):
        self.condition = condition
        self.body = body
    def __repr__(self): 
        return f"Loop: while ({self.condition}) {self.body}"

class StructNode(BaseNode):
    def __init__(self, name: str, list_item: dict[str, str]|None=None):
        self.name = name
        if list_item is None: self.l_item = {}
        else: self.l_item = list_item
    def __repr__(self):
        return f"Struct {self.name}: {{{', '.join(f'{k}: {v}' for k, v in self.l_item.items())}}}"

if __name__ == "__main__":
    print("[info]: This file only for import.")
    input("Press Enter to exit...")