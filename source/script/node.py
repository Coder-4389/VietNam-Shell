# app module
from source.script.typedef import Vtype

class BaseNode(): 
    def __init__(self): ...
    def __repr__(self): ...

class ValueNode(BaseNode):
    def __init__(self, value: any=None, _type: Vtype=None): 
        self.value = value
        self.type = _type
    def __repr__(self): 
        return f"Value: {self.value}, Type: {self.type}"

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

class BlockNode(BaseNode):
    def __init__(self, statements: list[BaseNode]=[]):
        self.statements = statements
    def __repr__(self): 
        return "Block: {\n" + "\n".join(map(str, self.statements)) + "\n}"

class FuncNode(BaseNode):
    def __init__(self, name: str="", params: list[str]=[], body: list[BaseNode]=None):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self): 
        return f"Func: {self.name}({', '.join(self.params)}) {self.body}"

class ReturnNode(BaseNode):
    def __init__(self, value: BaseNode=None, _type: Vtype=None):
        self.value = value
        self.type = _type
    def __repr__(self): 
        return f"Return: {self.value}"

class SpaceNode(BaseNode):
    def __init__(self, name, statements: list[BaseNode]=[]):
        self.name = name
        self.statements = statements
    def __repr__(self): 
        return f"{self.name} Space: "+"{\n"+"\n".join(map(str, self.statements))+"\n}"

class CondNode(BaseNode):
    def __init__(self, left: BaseNode, op: str, right: BaseNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"Condition: ({self.left} {self.op} {self.right})"

class IfNode(BaseNode):
    def __init__(self, condition: BaseNode=None, true_block: list[BaseNode]=None, false_block: list[BaseNode]=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
    def __repr__(self): 
        return f"If: if ({self.condition}) {self.true_block} else {self.false_block}"

class LoopNode(BaseNode):
    def __init__(self, condition: BaseNode=None, body: list[BaseNode]=None):
        self.condition = condition
        self.body = body
    def __repr__(self): 
        return f"Loop: while ({self.condition}) {self.body}"

class StructNode(BaseNode):
    def __init__(self, name: str, list_item: dict[str, Vtype]|None=None):
        self.name = name
        if list_item is None: self.l_item = {}
        else: self.l_item = list_item
    def __repr__(self):
        return f"Struct {self.name}: {{{', '.join(f'{k}: {v}' for k, v in self.l_item.items())}}}"

class CallNode(BaseNode):
    def __init__(self, name: str="", args: list[BaseNode]=[]):
        self.name = name
        self.args = args
    def __repr__(self): 
        return f"Call: {self.name}({', '.join(map(str, self.args))})"

class VarNode(BaseNode):
    def __init__(self, name: str="", value: BaseNode=None, _type: Vtype=None):
        self.name = name
        self.value = value
        self.type = _type
    def __repr__(self): 
        return f"Var: {self.name}"

class AccessNode(BaseNode):
    def __init__(self, space: str=None, _object: str=None, data: BaseNode=None):
        self.space = space
        self.object = _object
        self.data = data
    def __repr__(self):
        return f"From {self.space} space: use {self.object} ({self.data})"
