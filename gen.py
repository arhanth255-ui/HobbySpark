from parser import *
from lexer import *
from nodes import *
from instructions import *
from vm import *

class Function:
	def __init__(self, name, args, bytecode, funcpool, defaults) -> None:
		self.name=name
		self.args=args
		self.bytecode=bytecode
		self.funcpool = funcpool
		self.defaults = defaults
	@property
	def arity(self): return self.args.__len__()
	@property
	def required_arity(self): return self.args.__len__()-self.defaults.__len__()
	def run(self, vars_:dict, environment:Environment):
		if len(vars_)<self.required_arity or len(vars_)>self.arity:
			raise TypeError("Unexpected number of arguments: ", len(vars_))
		new_args = dict(vars_)

		# fill missing arguments
		for name, default in zip(
			self.args[-len(self.defaults):],
			self.defaults
		):
			if name not in new_args:
				new_args[name] = default

		newvm = VM(self.bytecode, self.funcpool, Environment(environment))
		for var, value in new_args.items():
			environment.set(var, value)
		out=newvm.run()
		return out

class Generator:
	def __init__(self, nodes) -> None:
		self.nodes:list = nodes
		self.bytecode = []
		self.current_index = 0
		self.current_loop = None
		self.breaks = []
		self.funcpool = []
		self.stop=False

	def run(self):
		for a in self.nodes:
			self.visit(a)
			if isinstance(a, (VariableNameNode)): self.add(op.POP)

		if not self.stop: self.bytecode.append(op.HALT)
		return self.bytecode, self.funcpool

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
		jumps=[]
		self.visit(node.condition)
		self.add(op.JUMP_IF_FALSE)
		to_jump = self.add(None)

		for stmt in node.body:
			self.visit(stmt)

		self.add(op.JUMP)
		jumps.append(self.add(None))

		if node.elifs:
			for el in node.elifs:
				self.patch(to_jump)
				self.visit(el.condition)
				self.add(op.JUMP_IF_FALSE)
				to_jump = self.add(None)
				for n in el.body:
					self.visit(n)
				self.add(op.JUMP)
				jumps.append(self.add(None))
		if node.else_:
			self.patch(to_jump)
			for n in node.else_.body:
				self.visit(n)
			for j in jumps:
				self.patch(j)
			return
		self.patch(to_jump)
		for j in jumps:
				self.patch(j)

	def c_WhileLoopNode(self, node:WhileLoopNode):
		self.current_loop=self.bytecode.__len__()
		self.visit(node.condition)
		self.add(op.JUMP_IF_FALSE)
		jump = self.add(None)
		for n in node.body: self.visit(n)
		self.add(op.JUMP)
		self.add(self.current_loop)
		self.patch(jump)
		for n in self.breaks: self.patch(n)

	def c_ContinueNode(self, node:ContinueNode):
		self.add(op.JUMP)
		self.add(self.current_loop)

	def c_BreakNode(self, node:BreakNode):
		self.add(op.JUMP)
		self.breaks.append(self.add(None))

	def c_CallNode(self, node:CallNode):
		print(node)
		if node.name.name == "print":
			self.visit(node.args[0])
			self.add(op.PRINT)
			return
		for a in node.args:
			self.visit(a)
		self.add(op.CALL)
		self.add(node.args.__len__())
		self.add(node.name.name)
		
	def c_FunctionDefineNode(self, node:FunctionDefineNode):
		name = node.name
		args=[]
		defaults={}
		for a in node.args:
			assert isinstance(a, ArgNode), "Wrong AST"
			args.append(a.name)
			if a.default is not None:
				
				try:defaults[a.name]=int(a.default.value)
				except Exception:
					default[a.name]=a.default.value
		new = Generator(node.body)
		bytecode, funcpool=new.run()
		self.funcpool.append(Function(
				name,
				args,
				bytecode, funcpool, defaults
			))
	def c_ReturnNode(self, node:ReturnNode):
		self.stop=True
		self.visit(node.value)
		self.add(op.RETURN)


	def visit_unsup(self, node):
		raise SyntaxError()
