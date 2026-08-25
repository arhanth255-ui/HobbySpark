from instructions import *

class Environment:
	def __init__(self, parent=None) -> None:
		self.vars = {}
		self.parent = parent
	def get(self, name):
		if name in self.vars:
			return self.vars[name]
		elif self.parent is not None:
			return self.parent.get(name)
		else:
			raise NameError("The variable is not declared", name=name)
	def set(self, name, value):
		self.vars[name]=value

class VM:
	def __init__(self, bytecode = [op.PUSH, 12, op.PUSH,14,op.ADD,op.HALT, op.PUSH, 12]) -> None:
		self.ip = 0
		self.bytecode = bytecode
		self.stack = []
		self.variables = Environment()

	def push(self, add):self.stack.append(add)

	def pop(self): return self.stack.pop()
	def current(self):
		a= self.bytecode[self.ip]
		self.ip+=1
		return a
	def run(self):
		while self.ip<len(self.bytecode):
			self.instruction = self.bytecode[self.ip]
			self.ip+=1
			match self.instruction:
				case op.HALT:
					print("RAN")
					return self.stack.pop() if self.stack else None
				case op.PUSH:
					value = self.bytecode[self.ip]
					self.ip+=1
					self.push(value)
				case op.ADD:
					value1 = self.pop()
					value2 = self.pop()
					self.push(value1+value2)
				case op.SUB:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1-value2)
				case op.MUL:
					value1 = self.pop()
					value2 = self.pop()
					self.push(value1*value2)
				case op.DIV:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1/value2)
				case op.STORE:
					val = self.current()
					self.variables.set(val,self.pop())
				case op.LOAD:
					val = self.current()
					self.push(self.variables.get(val))
				case op.EQ:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1==value2)
				case op.NEQ:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1!=value2)
				case op.LT:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1<value2)
				case op.LTE:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1<=value2)
				case op.GT:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1>=value2)
				case op.GTE:
					value2 = self.pop()
					value1 = self.pop()
					self.push(value1>=value2)
				case op.JUMP:
					self.ip = self.bytecode[self.ip]

				case op.JUMP_IF_FALSE:
					target = self.bytecode[self.ip]
					self.ip += 1
					val = self.pop()
					if val is False:
						self.ip = target
				case op.POP:
					self.pop()



