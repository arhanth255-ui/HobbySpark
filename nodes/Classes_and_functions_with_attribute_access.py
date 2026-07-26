from .Helpers import *
import nodes.Classes_and_functions_with_attribute_access as attr
import nodes.Types as typ

#Attribute access for classes and function calling.
class CallNode(Node):
    def __init__(self, name, args, kwargs:dict):
        self.name,self.args,self.kwargs=name,args,kwargs
        
class MethodCallNode(Node):
    def __init__(self, obj, name, args, kwargs):
        self.obj,self.name,self.args, self.kwargs=obj,name,args,kwargs

class AttributeAccessNode(Node):
    def __init__(self, obj, name):
        self.obj,self.name=obj,name

class DecoratorNode(Node):
    def __init__(self, name, args, kwargs):
        self.name,self.args,self.kwargs=name,args,kwargs

#Defining
class FunctionDefineNode(Node):
    def __init__(self,name,args,body,return_type,decors=[]):
        self.name,self.args,self.body,self.return_type,self.decors=name,args,body,return_type,decors

class AsyncFunctionDefineNode(Node):
    def __init__(self,name,args,body,return_type,decors=[]):
        self.name,self.args,self.body,self.return_type,self.decors=name,args,body,return_type,decors

class ClassDefineNode(Node):
    def __init__(self, name, body,decors,parents=None):
        self.name,self.body,self.parents,self.decors=name,body,parents,decors

#Return, Await and Yield
class ReturnNode(Node):
    def __init__(self, value):
        self.type_,self.value=get_type(value)

class YieldNode(Node):
    def __init__(self, value, from_):
        self.type_,self.value=get_type(value)
        self.from_=from_

class AwaitNode(Node):
    def __init__(self, func):
        self.func=func

#Get_type helper
def get_type(val):
    match val:
        case None:
            return "NONE",val
        case typ.ListNode():
            return "LIST",val
        case typ.DictNode():
            return "DICTIONARY",val
        case typ.TupleNode():
            return "TUPLE",val
        case typ.NumberNode():
            return "NUMBER",val
        case typ.StringNode():
            return "STRING",val
        case typ.BoolNode():
            return "BOOL",val
        case attr.CallNode()|attr.MethodCallNode():
            return "CALL",val
        case typ.VariableNameNode():
            return "VARIABLE_NAME",val
        case attr.AttributeAccessNode():
            return "ATTRIBUTE_ACCESS",val
        case _:
            return "GUESS",val
