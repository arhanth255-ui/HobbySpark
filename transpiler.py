from parser import *
from lexer import *
from json import load, dumps
from pathlib import Path
raw_data = {}
folder=Path.home()/"AppData"/"Roaming"/"HobbySpark transpiler"
file=folder/"ClassData.json"
with open(file) as f:
	raw_data = load(f)["special"]
data={}
for dat in raw_data:
	data[dat["name"]] = dat
def get_op(op):
	if op == TT_ADD:
		return "+"
	elif op == TT_MINUS:
		return "-"

	elif op == TT_MUL:
		return "*"
	elif op == TT_DIV:
		return "/"

	elif op == TT_POWER:
		return "^"
	elif op == TT_FLOOR_DIV:
		return "//"
	elif op == TT_MODULUS:
		return "%"
	elif op == TT_EQ:
		return "=="
	elif op == TT_NEQ:
		return "!="

	elif op == TT_GT:
		return ">"
	elif op == TT_GTE:
		return ">="

	elif op == TT_LT:
		return "<"
	elif op == TT_LTE:
		return "<="


def get_ctype(node, classes=[], orig:CallNode = CallNode("",[], {})):
	if node in ("NUMBER","int"):
		return "int"
	elif node in ("STRING","str"):
		return "String"
	elif node in ("BOOL","bool"):
		return "bool"
	elif node == "LIST":
		return "vector<>"
	elif node == "TUPLE":
		return "tuple<>"
	elif node == "None":
		return "void"
	elif (orig.name if isinstance(orig, CallNode) else "") in  classes and node=="CALL":
		print("ENETR")
		return orig.name
	else:
		return "auto"

class Result:
	def __init__(self, cpp, is_func=False, is_import=False, is_var=False, adder = "", semi=False) -> None:
		self.cpp = cpp
		self.is_func = is_func
		self.is_import = is_import
		self.is_var = is_var
		self.semi = semi
		self.adder = adder

	def __getitem__(self, index):
		if index==0: return self.cpp
		if index==1: return self.is_func
		if index==2: return self.is_import
		if index==3: return self.is_var
		if index==4: return self.semi
	@staticmethod
	def join(st = "\n", iterable = []):
		l = []
		for n in iterable:
			if isinstance(n, Result):
				l.append(n.cpp)
				l.append(n.adder)

			else:
				l.append(n)
		return st.join(l)


methods = {
	"__init__":("CONSTRUCTOR", "init"),
	"__add__":("auto operator+","shared"),
	"__sub__":("auto operator-","shared"),
	"__mul__":("auto operator*", "shared"),
	"__truediv__":("auto operator/", "shared"),
	"__eq__":("auto operator==", "shared"),
	"__neq__":("auto operator!=", "shared"),
	"__lt__":("auto operator<", "shared"),
	"__lte__":("auto operator<=", "shared"),
	"__gt__":("auto operator>", "shared"),
	"__gte__":("auto operator>=", "shared"),
	"__getitem__":("auto operator[]", "shared"),
	"__setitem__":("&auto operator[]", "shared")
}

class DunderMethodHelper:
	def __init__(self,method:FunctionDefineNode, give_var=False, scope = None, in_=False, in_class=False, cur_class_arg="", cur_class_scope=None, in_method=False, classes=None, cur_Class=None, vars_and_Classes = {}) -> None:
		self.obj=method
		self.method_name, self.full = methods[method.name]
		self.give_var=give_var
		self.vars=scope if scope is not None else [[]]
		self.newvars=[]
		self.block_vars=[]
		self.orig_vars=[]
		self.in_=in_
		self.in_class=in_class
		self.cur_class_arg = cur_class_arg
		self.cur_class_scope = cur_class_scope if cur_class_scope is not None else []
		self.in_method=in_method
		self.classes=classes+list(data.keys()) if classes is not None else list(data.keys())
		self.vars_and_Classes=vars_and_Classes
		self.number = 0

		if self.method_name == "CONSTRUCTOR":
			self.method_name, self.full = f"{cur_Class}", "init"
			self.ran = self.make()

		else:
			self.ran = self.make()

	def make(self):
		if hasattr(self, self.full):
			return getattr(self, self.full)()

	def visit(self, node):
		new_tra=Transpiler(ProgramNode([]),scope=self.get_cur_scope(),in_class=self.in_class,cur_class_arg=self.cur_class_arg,cur_class_scope=self.cur_class_scope, in_method=self.in_method, classes=self.classes, vars_and_Classes= self.vars_and_Classes)
		return new_tra.visit(node)[0], False,False,False

	def get_cur_scope(self):
		full=[]
		for sc in self.vars:
			full.extend(sc)
		return [full]

	def init(self):
		full_output=[f"{self.method_name} ({','.join([self.visit(n)[0] for n in self.obj.args if n.type_ != "Class_"])}){{"]
		print("fullo", ','.join([self.visit(n)[0] for n in self.obj.args if n.type_ != "Class_"]))

		self.vars.append([])
		self.vars[-1].extend([n.name for n in self.obj.args])
		self.newvars.extend([{
						"name":obj.name,
						"type":get_ctype(obj.type_)
					} for obj in self.obj.args])

		new_tra=Transpiler(ProgramNode(self.obj.body),scope=self.get_cur_scope(),in_class=self.in_class,cur_class_arg=self.cur_class_arg, cur_class_scope=self.cur_class_scope, in_method=self.in_method, classes=self.classes, vars_and_Classes= self.vars_and_Classes)
		new_tra.cur_class_arg = [n for n in self.obj.args if n.type_ == "Class_"][0]
		new_tra.in_method=True
		body=new_tra.translate_body()
		
		self.cur_class_scope=new_tra.cur_class_scope
		full_output.extend(body)
		full_output.append("}")
		self.vars.pop(-1)

		return "\n".join(full_output)

	def shared(self):
		full_output=[f"{self.method_name}({','.join([self.visit(n)[0] for n in self.obj.args if n.type_ != "Class_"])}){{"]
		print("fullo", ','.join([self.visit(n)[0] for n in self.obj.args if n.type_ != "Class_"]))

		self.vars.append([])
		self.vars[-1].extend([n.name for n in self.obj.args])
		self.newvars.extend([{
						"name":obj.name,
						"type":get_ctype(obj.type_)
					} for obj in self.obj.args])
		new_tra=Transpiler(ProgramNode(self.obj.body),scope=self.get_cur_scope(),in_class=self.in_class,cur_class_arg=self.cur_class_arg, cur_class_scope=self.cur_class_scope, in_method=self.in_method, classes=self.classes, vars_and_Classes= self.vars_and_Classes)
		new_tra.cur_class_arg = [n for n in self.obj.args if n.type_ == "Class_"][0]
		new_tra.in_method=True
		body=new_tra.translate_body()
		
		self.cur_class_scope=new_tra.cur_class_scope
		full_output.extend(body)
		full_output.append("}")
		self.vars.pop(-1)

		return "\n".join(full_output)

	




		
class UnsupportedFeatureError(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(" ".join(args))

class Transpiler:
	def __init__(self,
				 nodes,
				 give_var=False, 
				 scope = None, 
				 in_=False, 
				 in_class=False, 
				 cur_class_arg="", 
				 cur_class_scope=None, 
				 in_method=False, 
				 classes=None, 
				 cur_Class="", 
				 vars_and_Classes=None, 
				 vars_and_types = None, 
				 already_added = None, 
				 already_added_names=None,
				 updaters = {}
				 ) -> None:
		self.nodes=nodes.body
		self.give_var=give_var
		self.vars=scope if scope is not None else [[]]
		self.newvars=[]
		self.block_vars=[]
		self.orig_vars=[]
		self.in_=in_
		self.in_class=in_class
		self.cur_class_arg = cur_class_arg
		self.cur_class_scope = cur_class_scope if cur_class_scope is not None else []
		self.in_method=in_method
		self.classes=classes+list(data.keys()) if classes is not None else list(data.keys())
		self.cur_Class = cur_Class
		self.vars_and_Classes:dict=vars_and_Classes if vars_and_Classes is not None else {}
		self.vars_and_types:dict=vars_and_types if vars_and_types is not None else {}
		self.board = ""
		self.already_added = already_added if already_added is not None else []
		self.already_added_names = already_added_names if already_added_names is not None else []
		self.updaters:dict = updaters
		self.pins:list = []

	def translate(self):
		output = []
		imports=[]
		funcs=[]
		extras=[]
		vars_=[]
		adders = []
		with open(folder/"BoardsData.json", "r") as f:
			boards = load(f)
			print("ENTER", repr(self.board[:-2]))
			if self.board[:-2] in boards.keys():
				print("ENTER")
				pins:dict = boards[self.board[:-2]]
				pins:dict = {pin:actual for pin,actual in pins.items() if not pin.isdigit()}
				for pin, actual in pins.items():
					self.pins.append(pin)
			
		for node in self.nodes:
			cpp:Result = self.visit(node)
			cpp.cpp = f"{cpp.cpp};" if cpp.semi else cpp.cpp
			if cpp.is_func:
				funcs.append(cpp.cpp)
			elif cpp.is_import:
				imports.append(cpp.cpp)
			elif cpp.is_var:
				vars_.append(cpp.cpp)
			else:
				extras.append(cpp.cpp)

		with open(folder/"BoardsData.json", "r") as f:
			boards = load(f)
			print("ENTER", repr(self.board[:-2]))
			if self.board[:-2] in boards.keys():
				print("ENTER")
				pins:dict = boards[self.board[:-2]]
				pins:dict = {pin:actual for pin,actual in pins.items() if not pin.isdigit()}
				for pin, actual in pins.items():
					output.append(f"#define {pin} {actual}")
		output.append("#include \"package.h\"  \n")

		ifs = []
		print("UPDATERS", self.updaters)
		for t,n in self.updaters.items():
			update = t[0]
			value = t[1]
			print("UPDATE", self.updaters)
			print("VALUE", value)
			print("N",n)
			ifs.append(f"if ({update} {'>' if t[2] else '=='} {value}){{\n{n};\n}}")
		
		output.extend(imports)
		output.extend(vars_)
		output.extend(funcs)
		output.append(
f"""void wait(unsigned long time, float unit){{
	unsigned long end = millis() + (time*unit);

	while (millis() < end)
	{{
		{"\n".join(ifs)}
		{"\n".join(self.already_added)}

	}}
}}""")
		output.append("void setup(){ \n")
		output.extend(extras)
		output.append("}\n")
		output.append("void loop() {\n")

		output.extend(ifs)
		output.extend(self.already_added)
		output.append("}")
		return output

	def translate_body(self):
		output = []
		imports=[]
		funcs=[]
		extras=[]
		adders=[]
		vars_=[]
		for node in self.nodes:
			cpp:Result = self.visit(node)
			cpp.cpp = f"{cpp.cpp};" if cpp.semi else cpp.cpp
			if cpp.is_func:
				funcs.append(cpp.cpp)
			elif cpp.is_import:
				imports.append(cpp.cpp)			
			elif cpp.is_var:
				print("ADDING TO VARS:", cpp.cpp)
				vars_.append(cpp.cpp)
			else:
				extras.append(cpp.cpp)
				print("GOT_EXTRA WITH ADDER", repr(cpp.adder))
		output.extend(imports)
		output.extend(vars_)
		output.extend(funcs)
		output.extend(extras)
		return output

	def visit(self, node:Node):
		name = "visit_"+node.__class__.__name__
		m = getattr(self, name) if hasattr(self, name) else getattr(self, "visit_unsup")
		return m(node)

	def visit_BiNopNode(self, node:BiNopNode):
		return Result(f"{self.visit(node.a)[0]}{get_op(node.op)}{self.visit(node.b)[0]}")

	def visit_UnaryOpNode(self, node:UnaryOpNode):
		return Result(f"{get_op(node.op)}{self.visit(node.a)[0]}")

	def visit_NumberNode(self,node:NumberNode):
		return Result(f"{node.value}")

	def visit_StringNode(self, node:StringNode):
		return Result(f'"{node.value}"')

	def visit_BoolNode(self, node:BoolNode):
		return Result(f"{'true' if node.value=="TRUE" else "false"}")

	def visit_VariableNameNode(self,node:VariableNameNode):
		return Result(f"{node.name}")

	def visit_VariableAssignNode(self, node:VariableAssignNode):
		left=self.visit(node.left)[0]
		right=self.visit(node.right)
		type_=get_ctype(node.type,self.classes, node.right)
		for i in self.newvars:
			if self.visit(node.right)[0] == i["name"]:
				type_=i["type"]
		if (isinstance(node.right, CallNode) and not node.right.name.name in self.classes) or not isinstance(node.right, CallNode):
			self.newvars.append(
					{
						"name":left,
						"type":type_,
						"value":self.visit(node.right)
					}
				)

			self.orig_vars.append(
					{
						"name":left,
						"type":type_,
						"value":node.right
					}
				)
			
			if self.in_method and isinstance(node.left, AttributeAccessNode) and node.left.obj.name == self.cur_class_arg.name:
				self.cur_class_scope.append(
					{
						"name":left,
						"type":type_,
						"value":self.visit(node.right)[0]
					}
				)



		if left not in self.get_cur_scope():
			self.vars[-1].append(left)
			right:str=self.visit(node.right)[0]
			if type_=="vector<>":
				type__=self.list_type(node.right)

				return Result(f"{type__ if not self.in_class and  (isinstance(node.left, AttributeAccessNode) and node.left.obj.name == self.cur_class_arg.name) else 'this->'} {left} = {right} "if not self.give_var else f"{left} = {right}", False, False,"",True ,True)  
			
			elif type_=="tuple<>":
				return Result(self.make_tuple(left, right, node), False, False, "",True ,True)

			elif isinstance(node.right, CallNode) and node.right.name.name in self.classes:
				print("hello")
				kew_word=""
				for k,v in node.right.kwargs.items():
					v=self.visit(v)[0]
					kew_word+=f"{',' if len(node.right.args)>0 else ''}{k}={v}"

				args = []
				classes = [n["name"] for n in raw_data]
				n = 0
				for arg in node.right.args:
					classname = self.visit(node.right.name)[0]

						
					if self.visit(node.right.name)[0] not in classes or str(n) not in raw_data[classes.index(self.visit(node.right.name)[0])]["pin_args"]:
						args.append(self.visit(arg)[0])
					else:
						catalog:dict = raw_data[classes.index(self.visit(node.right.name)[0])]["pin_args"]
						if str(n) in catalog:
							args.append(arg.value.upper() if isinstance(arg.value,str) and arg.value.upper() in self.pins else arg.value)
						else:
							args.append(self.visit(arg)[0])
					n+=1
				args = [str(arg_) for arg_ in args]
				self.newvars.append(
					{
						"name":left,
						"type":node.right.name.name,
						"value":self.visit(node.right)
					}
				)

				self.orig_vars.append(
					{
						"name":left,
						"type":node.right.name.name,
						"value":node.right
					}
				)
			
				if self.in_method and isinstance(node.left, AttributeAccessNode) and node.left.obj.name == self.cur_class_arg.name:
					self.cur_class_scope.append(
						{
						"name":left,
						"type":node.right.name,
						"value":self.visit(node.right)[0],
						"raw_val":left
						}
					)

				print("type",type_)
				print("ke",left)
				print("rig",right)
				print("ENDS")

				if self.in_class and isinstance(node.left, AttributeAccessNode) and node.left.obj.name == self.cur_class_arg.name:
					print("left: ", left)
					return Result(f"{ "this->"} {left[6:] if left.startswith('this->') else left}  = {self.vars_and_Classes[left[6:] if left.startswith('this->') else left]}({",".join(args)} {kew_word})", is_var=True, semi=True)
				else:
					print("IS:",node.right.name.name in self.vars_and_Classes.keys())
					print("SELF.vars_and_Classes", self.vars_and_Classes)
					print("LEFT", repr(left))
					if left in self.vars_and_Classes:
						return Result(f"{left[6:] if left.startswith('this->') else left} = {self.vars_and_Classes[left[6:] if left.startswith('this->') else left]}({','.join(args)} {kew_word})",is_var=True, semi=True)
					else:
						self.vars_and_Classes[left] = node.right.name.name
						return Result(f"{node.right.name.name} {left}({','.join(args)} {kew_word})",is_var=True, semi=True)
			print("SELF.NEWVARS: ", self.newvars)
			cur_type  = ""
			already_seen = []
			for n in self.orig_vars:
				if n["name"] not in already_seen:
					already_seen.append(n["name"])
					if n["name"]==left:
						if n["type"] in self.classes:
							cur_type = n["value"].name.name 
							print("ctype: ", cur_type)
						else:
							cur_type = get_ctype(n["type"]) if n["type"] not in ["String", "int", "bool", "void", "tuple<>", "vector<>"] else n["type"]
						print("cur_type", cur_type, "For ", n["type"])
			
			rhs_type = get_ctype(node.type, self.classes, node.right)

			print("LHS TYPE:", repr(cur_type))
			print("RHS TYPE:", repr(rhs_type))
			print(cur_type)
			if cur_type != get_ctype(node.type, self.classes, node.right) and cur_type!="auto":
				raise UnsupportedFeatureError("Object of type ", cur_type, " is not convertible to ", node.type, "Name of variable:  ", left)

			if self.in_class and isinstance(node.left, AttributeAccessNode) and node.left.obj.name == self.cur_class_arg.name:
				print("enter")
				return Result( f"this-> {left[6:] if left.startswith('this->') else left} = {right}" if not self.give_var else f"{left} = {right}", False, False, False,True ,True)
			else:
				return Result(f"{type_} {left[6:] if left.startswith('this->') else left} = {right}" if not self.give_var else f"{left}= {right}", False, False, False,True ,True)

		return Result(f"{''if not self.in_class and  (isinstance(node.left, AttributeAccessNode) and node.left.obj.name == self.cur_class_arg.name) else 'this->'}{left} = {right[0]}", False, False,False,True ,True)

	def tuple_type(self,node):
		parts = []

		for item in node.items:
			t = get_ctype(get_type(item)[0],self.classes)

			if t == "tuple<>":
				parts.append(self.tuple_type(item))

			elif t=="vector<>":
				parts.append(self.list_type(item))

			else:
				parts.append(t)

		return f"std::tuple<{','.join(parts)}>"

	def list_type(self, node):
		if not node.items:
			raise UnsupportedFeatureError("Empty lists without annotation is not allowed. ")

		first=node.items[0]
		base=get_ctype(get_type(first)[0], self.classes)

		if base=="vector<>":
			return f"std::vector<{self.list_type(first)}>"

		elif base == "tuple<>":
			return f"std::vector<{self.tuple_type(first)}>"

		else:
			return f"std::vector<{base}>"

	def make_tuple(self,left,right, node:VariableAssignNode):
		type_=self.tuple_type(node.right)

		return f"{type_ if not self.in_class else 'this->'} {left} = {right}"

	def visit_ListNode(self, node:ListNode):
		type_=get_ctype(get_type(node.items[0])[0],self.classes) if len(node.items)!=0 else None
		if type_ is None:
			raise UnsupportedFeatureError("Empty lists without annotation is not allowed. ")
		vals=[]
		for val in node.items:
			vals.append(self.visit(val)[0])
		return Result(f"{{ {",".join(vals)} }}")

	def visit_TupleNode(self,node:TupleNode):
		type_=get_ctype(get_type(node.items[0])[0], self.classes) if len(node.items)!=0 else None
		if type_ is None:
			raise UnsupportedFeatureError("Empty tuples without annotation is not allowed. ")
		vals=[]
		for val in node.items:
			vals.append(self.visit(val)[0])
		return Result(f"{{ {",".join(vals)} }}")

	def visit_IfConditionNode(self, node:IfConditionNode):
		full_output=[]
		cond= self.visit(node.condition)
		if_new_tra = self.gen_transpiler(node.body)
		if_body=if_new_tra.translate_body()
		elif_bodies=[]
		elif_newtras=[]
		elif_block=[]
		elif_newvars=[]
		for elif_ in node.elifs:
			elif_newtra=self.gen_transpiler(node.body)
			elif_newtras.append(elif_newtra)
			elif_bodies.append((elif_newtra.translate_body(),elif_.condition))

		for tra in elif_newtras:
			elif_block.extend(tra.block_vars)

		for newvar in elif_newtras:
			elif_newvars.extend(newvar.newvars)

		else_new_tra = self.gen_transpiler(node.body) if node.else_ else None
		else_body=if_new_tra.translate_body() if else_new_tra is not None else None

		total=[]
		total.extend(if_new_tra.block_vars)
		total.extend(elif_block)
		if else_new_tra is not None:total.extend(else_new_tra.block_vars)

		new=[new_var for new_var in if_new_tra.newvars if new_var not in total]
		new.extend([new_var for new_var in elif_newvars if new_var not in total])
		if else_new_tra is not None:new.extend([new_var for new_var in else_new_tra.newvars if new_var not in total])
		total.extend(new)
		for var in total:
			if var["name"] not in self.get_cur_scope():
				self.block_vars.append(var)
				full = f"{var['type']} {var['name']};"

				if var["name"] not in self.vars[-1]:
					if not self.in_:
						self.vars[-1].append(var["name"])
						full_output.append(full)
		full_output.append(f"if ({cond[0]}){{ ")
		full_output.extend(if_body)
		full_output.append("}")
		for body,cond in elif_bodies:
			full_output.append(f"else if {self.visit(cond)}{{")
			full_output.extend(body)
			full_output.append("}")
		if else_new_tra is not None:
			full_output.append("else {")
			full_output.extend(else_body)
			full_output.append("}")
		return Result("\n\t".join(full_output))

	def visit_ElifConditionNode(self, node:ElifConditionNode):
		full_output=[]
		cond= self.visit(node.condition)
		new_tra = self.gen_transpiler(node.body)
		body=new_tra.translate_body()
		total=[]
		total.extend(new_tra.block_vars)
		new=[new_var for new_var in new_tra.newvars if new_var not in total]
		total.extend(new)
		for var in total:
			if var["name"] not in self.get_cur_scope():
				self.block_vars.append(var)
				full = f"{var['type']} {var['name']};"

				if var["name"] not in self.vars[-1]:
					if not self.in_:
						self.vars[-1].append(var["name"])
						full_output.append(full)
		full_output.append(f"else if ({cond[0]}){{ ")

		full_output.extend(body)
		full_output.append("}")
		return Result("\n".join(full_output))

	def visit_WhileLoopNode(self, node:WhileLoopNode):
		full_output=[]
		cond= self.visit(node.condition)
		new_tra = self.gen_transpiler(node.body)
		body=new_tra.translate_body()
		total=[]
		total.extend(new_tra.block_vars)
		new=[new_var for new_var in new_tra.newvars if new_var not in total]
		total.extend(new)
		for var in total:
			if var["name"] not in self.get_cur_scope():
				self.block_vars.append(var)
				full = f"{var['type']} {var['name']};"

				if var["name"] not in self.vars[-1]:
					if not self.in_:
						self.vars[-1].append(var["name"])
						full_output.append(full)
		full_output.append(f"while ({cond[0]}){{ ")
		full_output.extend(body)
		full_output.append("}")
		return Result("\n".join(full_output))

	def visit_ForLoopNode(self,node:ForLoopNode):
		full_output = []
		iterable_name = f"{node.var}"
		array=False
		num=None
		num2=None
		num3=None
		if isinstance(node.iterable, CallNode) and node.iterable.name=="range":
			iterable = self.visit(node.iterable)[0]
			num=self.visit(node.iterable.args[0])[0]
			num2=self.visit(node.iterable.args[1])[0] if len(node.iterable.args)>1 else None
			num3=self.visit(node.iterable.args[2])[0] if len(node.iterable.args)>2 else None

		elif isinstance(node.iterable, ListNode):
			iterable = self.visit(node.iterable)[0]
			array=True

		elif isinstance(node.iterable, VariableNameNode):
			var_names=[a["name"] for a in self.newvars]

			if node.iterable.name in var_names:
				val = self.orig_vars[var_names.index(node.iterable.name)]["value"]
				print("val", val)

				if isinstance(val, CallNode) and val.name=="range":
					iterable = node.iterable.name
					num=self.visit(val.args[0])[0]
					num2=self.visit(val.iterable.args[1])[0] if len(val.args)>1 else None
					num3=self.visit(val.args[2])[0] if len(val.args)>2 else None

				elif isinstance(val, ListNode):
					print("hello")
					iterable = node.iterable.name
					array=True

		else:
			raise UnsupportedFeatureError(f"Node {node} for 'for' loops is not supported.")

		
		new_tra=self.gen_transpiler(node.body)
		if not array:
			new_tra.newvars.append({
				"type":"int",
				"value":(num if num2 is not None else '0',False,False),
				"name":node.var
			})
		else:
			new_tra.newvars.append({
				"type":"auto",
				"value":(None,False,False),
				"name":node.var
			})
		body=new_tra.translate_body()
		
		total=[]
		total.extend(new_tra.block_vars)
		new=[new_var for new_var in new_tra.newvars if new_var not in total and new_var["name"] != iterable_name]
		total.extend(new)


		for var in total:
			print(var)
			if var["name"] not in self.get_cur_scope():
				self.block_vars.append(var)
				full = f"{var['type']} {var['name']};"

				if var["name"] not in self.vars[-1]:
					if not self.in_:
						self.vars[-1].append(var["name"])
						full_output.append(full)

		if not array:
			full_output.append(f"for (int {iterable_name} = {num if num2 is not None else '0'}; {iterable_name} < {num2 if num2 is not None else num}; {iterable_name} +={num3 if num3 else 1} ) {{")
		else:
			full_output.append(f"for (auto& {iterable_name} : {iterable})")
		full_output.extend(body)
		full_output.append("}")
		return Result("\n".join(full_output))


	def visit_ElseNode(self, node:ElseNode):
		full_output=[]
		new_tra = self.gen_transpiler(node.body)
		body=new_tra.translate_body()
		total=[]
		total.extend(new_tra.block_vars)
		new=[new_var for new_var in new_tra.newvars if new_var not in total]
		total.extend(new)
		for var in total:
			if var["name"] not in self.get_cur_scope():
				self.block_vars.append(var)
				full = f"{var['type']} {var['name']};"

				if var["name"] not in self.vars[-1]:
					if not self.in_:
						self.vars[-1].append(var["name"])
						full_output.append(full)

		full_output.append(f"else{{ ")
		full_output.extend(body)
		full_output.append("}")
		return Result("\n".join(full_output))

	def visit_FunctionDefineNode(self, node:FunctionDefineNode):
		if self.in_class:
			return Result(self.make_method(node),True)
		full_output=[f"{get_ctype(node.return_type if node.return_type is not None else "auto", self.classes)} {node.name}({','.join([self.visit(n)[0] for n in node.args])}){{"]
		self.vars.append([])
		self.vars[-1].extend([n.name for n in node.args])
		self.newvars.extend([{
						"name":obj.name,
						"type":obj.type_
					} for obj in node.args])
		new_tra=self.gen_transpiler(node.body)
		print("ORIGVARS FROM",new_tra.orig_vars)
		new_tra.orig_vars = self.orig_vars
		body=new_tra.translate_body()
		full_output.extend(body)
		full_output.append("}")
		self.vars.pop(-1)
		variables = [var.name for var in node.args]
		self.newvars = [obj for obj in self.newvars if obj["name"] not in variables]
		print("FULL_OUTPUT", full_output)
		return Result("\n".join(full_output),True)

	def make_method(self, node:FunctionDefineNode):
		full_output=[f"{get_ctype(node.return_type if node.return_type is not None else "auto", self.classes)} {node.name}({','.join([self.visit(n)[0] for n in node.args if n.type_ != "Class_"])}){{"]
		self.vars.append([])
		self.vars[-1].extend([n.name for n in node.args])

		self.newvars.extend([{
						"name":obj.name,
						"type":obj.type_
					} for obj in node.args])
		
		new_tra=self.gen_transpiler(node.body)
		new_tra.cur_class_arg = [n for n in node.args if n.type_ == "Class_"][0]
		new_tra.in_method=True
		if node.name in methods:
			return self.make_dunder(node)

		body=new_tra.translate_body()
		self.cur_class_scope=new_tra.cur_class_scope
		full_output.extend(body)
		full_output.append("}")
		self.vars.pop(-1)
		variables = [var.name for var in node.args]
		self.newvars = [obj for obj in self.newvars if obj["name"] not in variables]
		return "\n".join(full_output)

	def make_dunder(self, node:FunctionDefineNode):
		full_output = []
		self.vars.append([])
		self.vars[-1].extend([n.name for n in node.args])
		newvars = [name["name"] for name in self.newvars]
		tra = DunderMethodHelper(node,scope=self.get_cur_scope(),in_class=self.in_class,cur_class_arg=self.cur_class_arg,cur_class_scope=self.cur_class_scope, in_method=self.in_method, classes=self.classes, cur_Class=self.cur_Class)
		print("NEWTRA.self", tra.newvars)
		self.newvars.extend(tra.newvars)
		self.vars.pop()
		return tra.ran




	def visit_ArgNode(self, node:ArgNode):
		return_=f"{get_ctype(node.type_,self.classes)} {node.name} {'='+self.visit(node.default)[0] if node.default else ''}"
		return Result(return_)

	def visit_ReturnNode(self, node:ReturnNode):
		return Result(f"return ({self.visit(node.value)[0]})",semi=True)

	def visit_CallNode(self,node:CallNode):
		if self.visit(node.name)[0] =="set_board":
			self.board = [self.visit(n)[0] for n in node.args][0]
			return Result("//SetBoard")

		kew_word=""
		count=0
		for k,v in node.kwargs.items():
			count+=1
			v=self.visit(v)[0]
			kew_word+=f"{',' if len(node.args)>0 else ''}{k} = {v}"
		args = []
		classes = [n["name"] for n in raw_data]
		print("ARGS", node.args)
		n = 0
		for arg in node.args:
			classname = self.visit(node.name)[0]
			dat = ""
			if self.visit(node.name)[0] in classes:
				dat = raw_data[classes.index(self.visit(node.name)[0])]["pin_args"]
			if self.visit(node.name)[0] not in classes and str(n) not in dat:
				args.append(self.visit(arg)[0])
			else:
				print("ENTERED CATALOG")
				catalog:dict = raw_data[classes.index(self.visit(node.name)[0])]["pin_args"]
				for k,v in catalog.items():
					if str(n)==k:
						args.append(arg.value.upper() if isinstance(arg.value,str) else arg.value)
			n+=1
		args = [str(arg_) for arg_ in args]
		return_=f"{self.visit(node.name)[0]}({','.join(args)}{kew_word if kew_word else ""})"
		print(return_)
		return Result(return_,semi=True)

	def visit_MethodCallNode(self, node:MethodCallNode):
		kew_word=""
		count=0
		for k,v in node.kwargs.items():
			count+=1
			v=self.visit(v)[0]
			kew_word+=f"{',' if len(node.args)>0 else ''}{k} = {v}"

		if self.in_method and self.cur_class_arg.name == self.visit(node.obj)[0]:
			return f"this->{node.name}({','.join([self.visit(n)[0] for n in node.args])}{kew_word if kew_word else ""})", False,False,True
		classes = [n["name"] for n in raw_data if n["requires_updt"]]
		u_classes = [n["name"] for n in raw_data if n["requires_even"]]
		return_=f"{self.visit(node.obj)[0]}.{node.name}({','.join([self.visit(n)[0] for n in node.args])}{kew_word if kew_word else ""})"
		vars_ = [n["name"] for n in self.orig_vars]
		cond = None

		if self.visit(node.obj)[0] in vars_:
			cond = (self.orig_vars[vars_.index(self.visit(node.obj)[0])] )["value"]
		
		if self.visit(node.obj)[0] in classes or (isinstance(cond,CallNode) and self.visit(cond.name)[0] in classes):
			if self.visit(node.obj)[0] not in self.already_added_names:
				self.already_added.append(f"{self.visit(node.obj)[0]}.update();")
				self.already_added_names.append(self.visit(node.obj)[0])

		if self.visit(node.obj)[0] in u_classes or (isinstance(cond,CallNode) and self.visit(cond.name)[0] in u_classes):
			methods = [n["methods"] for n in raw_data if isinstance(cond,CallNode) and n["name"]==self.visit(cond.name)[0]][0]
			print("METHODS")
			big_data = {}
			print("DATA", dumps(data, indent=4))
			if self.visit(node.obj)[0] in u_classes or (isinstance(cond,CallNode) and node.name in methods):
				self.updaters[(f"{self.visit(node.obj)[0]}.update()", 'true' if methods[node.name]["arg"] is None  else self.visit(node.args[methods[node.name]["arg"]])[0],data[self.visit(cond.name)[0]]["big"] if isinstance(cond, CallNode) else False) ] = f"{self.visit(node.args[methods[node.name]["i"]])[0]}({'true' if methods[node.name]["arg"] is None else self.visit(node.args[methods[node.name]["arg"]])[0]})"
			
			return Result("")

		print("RETURN FOR ", node, "IS", return_, "AND ", self.orig_vars)
		result = Result(return_,semi=True)
		return result

	
	def visit_ClassDefineNode(self, node:ClassDefineNode):
		if "Board" in node.parents:
			return Result("")
		self.classes.append(node.name)
		self.vars.append([])
		full_output=[]
		full_output.extend([f"class {node.name}{{", "public:" if node.body else ""])
		new_tra = self.gen_transpiler(node.body)
		new_tra.in_class=True
		new_tra.cur_Class = node.name
		new_tra.vars_and_Classes, new_tra.newvars = self.find_vars(node.body)
		print("VARS GEN BY FIND VARS",new_tra.vars_and_Classes)
		print("NEWVARS GEN", new_tra.newvars)
		body=new_tra.translate_body()
		for var in new_tra.cur_class_scope:
			if var["name"] not in self.get_cur_scope()[0]:
				self.block_vars.append(var)
				self.vars[-1].append(var)
				type_ = var["type"]

				print("NEWVARS", self.newvars)
				print("NEWVARS123", new_tra.newvars)
				for var_dict in new_tra.newvars:
					if var_dict["name"] == (var['name'][6:] if var['name'].startswith('this->') else var['name']):
						type_=var_dict["type"]

				print(F"TYPE FOR {var["name"]} IS {type_}.")
				if isinstance(var["type"], VariableNameNode):
					print("TYPE", type_)
					full = f"{type_.name} {var["raw_val"] if not var["raw_val"].startswith("this->") else var["raw_val"][6:]};"
				else:
					full = f"{type_} {var['name'][6:] if var['name'].startswith('this->') else var['name']};"
					print("full",full)

				if var["name"] not in self.vars[-1]:
					print("hello world!!!")
					if not self.in_:
						self.vars_and_Classes[var["name"]] = var["type"]
						print("added", var["type"])
						self.vars[-1].append(var["name"])
						full_output.append(full)


		full_output.extend(body)
		full_output.append("};")
		self.vars.pop(-1)
		self.in_class = False
		return Result("\n".join(full_output),True)

	def find_vars(self, nodes:list[Node], class_arg=""):
		variables = {}
		newvars = []
		class_arg = class_arg
		for node in nodes:
			if isinstance(node, VariableAssignNode) and isinstance(node.left, AttributeAccessNode) and self.visit(node.left.obj)[0] == class_arg:
				if node.left.name in variables:
					pass
				else:
					newvars.append({
							"name":node.left.name,
							"type":get_ctype(get_type(node.type)[0], self.classes)
						})
					variables[node.left.name] = get_ctype(get_type(node.right)[0] if get_type(node.right)[0] !="CALL" else node.right.name.name, self.classes)
			elif hasattr(node, "body"):
				if isinstance(node, FunctionDefineNode):
					class_arg = [arg.name for arg in node.args if arg.type_ == "Class_"][0]

				variables = variables|self.find_vars(node.body, class_arg)[0]
				newvars.extend(self.find_vars(node.body, class_arg)[1])
		print(f"NEWVARS {newvars}")
		return variables, newvars

	def visit_GetItemNode(self, node:GetItemNode):
		return_ = f"{self.visit(node.obj)[0]}[{self.visit(node.index)[0]}]"
		return Result(return_)

	def visit_SetItemNode(self, node:SetItemNode):
		return Result(f"{self.visit(node.getitem)[0]} = {self.visit(node.val)[0]}",semi=True)


	def visit_PassNode(self,node:PassNode):
		return Result("\n")

	def visit_AttributeAccessNode(self, node:AttributeAccessNode):

		if self.in_method and self.cur_class_arg.name == self.visit(node.obj)[0]:
			return Result(f"this->{node.name}")

		return Result(f"{self.visit(node.obj)[0]}.{node.name}")

	def get_cur_scope(self):
		full=[]
		for sc in self.vars:
			full.extend(sc)
		return [full]

	def visit_FromImportNode(self,node:FromImportNode):
		return Result("")

	def visit_BreakNode(self, node:BreakNode): return "break;"
	def visit_ContinueNode(self, node): return "continue;"

	def gen_transpiler(self, first, **kwargs):
		std = {
			"scope":self.get_cur_scope(),
			"in_class":self.in_class,
			"cur_class_arg":self.cur_class_arg,
			"cur_class_scope":self.cur_class_scope,
			"in_method":self.in_method,
			"classes":self.classes,
			"vars_and_Classes":self.vars_and_Classes,
			"already_added":self.already_added,
			"already_added_names":self.already_added_names,
			"updaters":self.updaters
		}
		std.update(**kwargs)
		tr = Transpiler(ProgramNode(first),**std)

		tr.orig_vars = self.orig_vars
		tr.newvars = self.newvars
		tr.block_vars = self.block_vars
		tr.in_class = self.in_class
		return tr

	def visit_unsup(self, node):
		raise UnsupportedFeatureError(f"Node {node} is unsupported.")

