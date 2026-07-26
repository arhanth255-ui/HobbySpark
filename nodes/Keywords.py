from .Helpers import *
#Placeholders
class ContinueNode(Node):
    pass

class BreakNode(Node):
    pass

class PassNode(Node):
    pass

#Lambdas and assert
class LamdaNode(Node):
    def __init__(self, args, action):
        self.args,self.action=args,action

class AssertNode(Node):
    def __init__(self, expr, message=None):
        self.expr,self.message=expr,message

#Error handling
class RaiseNode(Node):
    def __init__(self, error):
        self.error=error

class TryNode(Node):
    def __init__(self,body,excepts,else_,finally_):
        self.body,self.excepts,self.else_,self.finally_=body,excepts,else_,finally_

class ExceptNode(Node):
    def __init__(self, error, body, as_):
        self.error,self.body,self.as_=error,body,as_

class FinallyNode(Node):
    def __init__(self, body):
        self.body=body

class TryElseNode(Node):
    def __init__(self,body):
        self.body=body

#With and global
class WithNode(Node):
    def __init__(self, name, as_, body):
        self.name,self.as_,self.body=name,as_,body

class AsyncWithNode(Node):
    def __init__(self, name, as_, body):
        self.name,self.as_,self.body=name,as_,body

class GlobalNode(Node):
    def __init__(self, var):
        self.var=var

#####################################################
#Custom
#####################################################

#Raise if
class RaiseIfNode(Node):
    def __init__(self, expr, error=None):
        self.expr,self.error=expr,error


