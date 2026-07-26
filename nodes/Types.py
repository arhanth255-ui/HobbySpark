from .Helpers import *
#types 
class NumberNode(Node):
    def __init__(self,value):
        self.value=value

class StringNode(Node):
    def __init__(self,value):
        self.value=value

class FormattedStringNode(Node):
    def __init__(self,values:list):
        self.values=values

class BoolNode(Node):
    def __init__(self,value):
        self.value=value

class ListNode(Node):
    def __init__(self,items):
        self.items=items

class DictNode(Node):
    def __init__(self,items):
        self.items=items

class NoneNode(Node):
    pass

class TupleNode(Node):
    def __init__(self, items):
        self.items=items
        
class ImplicitTupleNode(Node):
    def __init__(self, items):
        self.items=items

class VariableNameNode(Node):
    def __init__(self, name):
        self.name=name
    
class VariableNameNode(Node):
    def __init__(self, name):
        self.name=name

class GeneratorNode(Node):
    def __init__(self,name,args,body,returns,decors=[]):
        self.name,self.args,self.body,self.returns,self.decors=name,args,body,returns,decors

class AsyncGeneratorNode(Node):
    def __init__(self,name,args,body,returns,decors=[]):
        self.name,self.args,self.body,self.returns,self.decors=name,args,body,returns,decors

class FstringExpression(Node):
    def __init__(self, expr, format):
        self.expr,self.format=expr,format

#List, tuple and dict helpers
class GetItemNode(Node):
    def __init__(self, obj, index):
        self.obj,self.index=obj,index
    

class SetItemNode(Node):
    def __init__(self, getitem, val):
        self.getitem,self.val=getitem,val
    
class SliceNode(Node):
    def __init__(self, obj, start=None, stop=None, tick=None):
        self.obj,self.start,self.end,self.tick=obj,start,stop,tick