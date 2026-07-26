from .Helpers import *
class ProgramNode(Node):
    def __init__(self, body):
        self.body=body

class ArgNode(Node):
    def __init__(self, name, type_, default=None, special=None):
        self.name,self.type_,self.default,self.special=name,type_,default,special