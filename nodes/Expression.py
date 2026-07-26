from .Helpers import *
import nodes.Classes_and_functions_with_attribute_access as c
#Basic math
class BiNopNode(Node):
    def __init__(self,a,op,b):
        self.a,self.b,self.op=a,b,op
    
class UnaryOpNode(Node):
    def __init__(self,op,a):
        self.op,self.a=op,a

#One liners
class ListComprehensionNode(Node):
    def __init__(self, iterable, variable, left, condition):
        self.iterable,self.variable,self.left,self.condition=iterable,variable,left,condition

class AsyncListComprehensionNode(Node):
    def __init__(self, iterable, variable, left, condition):
        self.iterable,self.variable,self.left,self.condition=iterable,variable,left,condition

class GeneratorComprehensionNode(Node):
    def __init__(self, iterable, variable, left, condition):
        self.iterable,self.variable,self.left,self.condition=iterable,variable,left,condition

class AsyncGeneratorComprehensionNode(Node):
    def __init__(self, iterable, variable, left, condition):
        self.iterable,self.variable,self.left,self.condition=iterable,variable,left,condition

class TernaryOperationNode(Node):
    def __init__(self, condition, true_val, false_val):
        self.condition,self.true_val,self.false_val=condition,true_val,false_val

class DictComprehensionNode(Node):
    def __init__(self, iterable, variable,
                 key, value, condition):
        self.iterable = iterable
        self.variable = variable
        self.key = key
        self.value = value
        self.condition = condition
class AsyncDictComprehensionNode(Node):
    def __init__(self, iterable, variable,
                 key, value, condition):
        self.iterable = iterable
        self.variable = variable
        self.key = key
        self.value = value
        self.condition = condition
#Variables

class VariableAssignNode(Node):
    def __init__(self, left, right):
        self.left=left
        self.type,self.right=c.get_type(right)

class VariableCompAssignNode(Node):
    def __init__(self, left, right, op):
        self.left=left
        self.op=op
        self.type,self.right=c.get_type(right)

