import types

from nodes import *
from lexer import *
from enum import IntEnum

class Types(IntEnum):
    INT = 0
    FLOAT = 1
    STRING = 2
    BOOL = 3
    UNKNOWN = 4

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)

class SemanticAnalyzer:
    def __init__(self, body_node:ProgramNode):
        self.nodes = body_node.body
        self.symbols = {}

    def analyze_semantically(self):
        results = []
        for node in self.nodes:
            node, semant = self.visit(node)
            results.append((node, semant))
        return results
    
    
    def visit(self, node:Node):
        name = "visit_"+node.__class__.__name__
        m = getattr(self, name) if hasattr(self, name) else getattr(self, "visit_unsup")
        return m(node)
    
    def visit_BiNopNode(self, node:BiNopNode):
        type = None
        a_sem = self.visit(node.a)[1] 
        b_sem = self.visit(node.b)[1]
        
        if node.op in (TT_EQ, TT_NEQ, TT_GT, TT_GTE, TT_LT, TT_LTE): type = Types.BOOL

        elif a_sem["type"]==b_sem["type"]:
            type = a_sem["type"]
            
        elif a_sem["type"]==Types.FLOAT and b_sem["type"]==Types.INT: type = Types.FLOAT

        elif a_sem["type"]==Types.INT and b_sem["type"]==Types.FLOAT: type = Types.FLOAT

        else:
            raise SemanticError(f"Cannot operate on operands of type {a_sem['type'] } and {b_sem['type']}")
        tree = {
                    "a":a_sem,
                    "b":b_sem,
                    "op":node.op,
                    "type":type
                }
        return node, tree

    def visit_UnaryOpNode(self, node:UnaryOpNode):
        tree = {
                    "a":self.visit(node.a)[1],
                    "op":node.op
                }
        return node, tree
    
    def visit_NumberNode(self, node:NumberNode):
        tree = {
                    "type":Types.FLOAT if isinstance(node.value, str) else Types.INT
                }
        return node, tree

    def visit_StringNode(self, node:StringNode):
        tree = {
                    "type":Types.STRING
            }
        return node, tree

    def visit_BoolNode(self, node:BoolNode):
        tree = {
                "type":Types.BOOL
            }
        return node, tree
    
    
    def visit_VariableAssignNode(self, node:VariableAssignNode):
        right_sem = self.visit(node.right)[1]
        tree = {
                    "right":right_sem,
                    "left":node.left.name,
                    "type":right_sem["type"]
                }
        self.symbols[node.left.name] = {"type":self.visit(node.right)[1]["type"]}
        print("Symbols", self.symbols)

        return node, tree

    def visit_VariableNameNode(self, node:VariableNameNode):
        type = self.symbols[node.name]["type"]
        tree = {
                "name": node.name,
                "type":type
                }
        return node, tree

    def visit_unsup(self, node):
        raise UnsupportedFeatureError(f"Node {node} is unsupported.")

    
