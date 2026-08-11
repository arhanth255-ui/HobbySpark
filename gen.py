from parser import *
from lexer import *
from nodes import *
from b import *

class Generator:
	def __init__(self, nodes) -> None:
		self.nodes:list = nodes
		self.bytecode = []
		self.current_index = 0

	def run(self):
		for a in self.nodes:
			self.visit(a)

		self.bytecode.append(op.HALT)
		return self.bytecode

	def visit(self, node):
		name = "c_"+node.__class__.__name__
		m = getattr(self, name) if hasattr(self, name) else getattr(self, "visit_unsup")
		return m(node)

	def add(self, adder):
		self.bytecode.append(adder)
		self.current_index = self.bytecode.__len__()-1
		return self.current_index

	def patch(self, index):
		self.bytecode[index]=len(self.bytecode)

	def c_NumberNode(self, node:NumberNode):
		self.bytecode.append(op.PUSH)
		self.bytecode.append(int(node.value))

	def c_BiNopNode(self, node:BiNopNode):
		self.visit(node.a); self.visit(node.b)
		if node.op == TT_ADD:
			SIGN = op.ADD
		elif node.op == TT_MINUS:
			SIGN = op.SUB

		elif node.op == TT_MUL:
			SIGN = op.MUL
		elif node.op == TT_DIV:
			SIGN = op.DIV

		elif node.op == TT_POWER:
			SIGN = op.ADD
		elif node.op == TT_FLOOR_DIV:
			SIGN = op.ADD
		elif node.op == TT_MODULUS:
			SIGN = op.ADD
		elif node.op == TT_EQ:
			SIGN = op.EQ
		elif node.op == TT_NEQ:
			SIGN = op.NEQ

		elif node.op == TT_GT:
			SIGN = op.GT
		elif node.op == TT_GTE:
			SIGN = op.GTE

		elif node.op == TT_LT:
			SIGN = op.LT
		elif node.op == TT_LTE:
			SIGN = op.LTE

		self.bytecode.append(SIGN)
		print("BYTE", self.bytecode)

	def c_VariableAssignNode(self, node:VariableAssignNode):
		self.visit(node.right)
		self.bytecode.append(op.STORE)
		self.bytecode.append(node.left.name)

	def c_VariableNameNode(self, node:VariableNameNode):
		self.bytecode.append(op.LOAD)
		self.bytecode.append(node.name)

	def c_IfConditionNode(self, node:IfConditionNode):
		self.visit(node.condition)
		self.add(op.JUMP_IF_FALSE)
		to_jump = self.add(None)

		for stmt in node.body:
			self.visit(stmt)

		self.patch(to_jump)



	def visit_unsup(self, node):
		raise SyntaxError()
