from .Helpers import *
import nodes.Classes_and_functions_with_attribute_access as attr
import nodes.Types as typ
#If conditions: (if, elif, else)
class IfConditionNode(Node):
    def __init__(self, condition, body, elifs=None, else_=None):
        self.condition,self.body=condition,body
        self.elifs=elifs
        self.else_=else_

class ElifConditionNode(Node):
    def __init__(self, cond, body):
        self.condition,self.body=cond,body

class ElseNode(Node):
    def __init__(self, body):
        self.body=body

#Loops: (while, for)
class WhileLoopNode(Node):
    def __init__(self, condition, body):
        self.condition,self.body=condition,body

class ForLoopNode(Node):
    def __init__(self, iterable, body, var):
        self.iterable,self.body,self.var=iterable,body,var

#Async loops:
class AsyncForLoopNode(Node):
    def __init__(self, iterable, body, var):
        self.iterable,self.body,self.var=iterable,body,var

#Matches
class MatchNode(Node):
    def __init__(self, cases, variable, default):
        self.cases,self.var,self.default=cases,variable,default

class CaseNode(Node):
    def __init__(self, val, body):
        self.val,self.body=val,body