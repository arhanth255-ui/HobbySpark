def make(name:str, args, arguments, method, method2=None):
	args_ = ""
	for i,arg in enumerate(args,1):
		args_+=f"{i}. {arg["name"]} - {arg["type"]} - {arg["e"]}. \n"
	doc_string = f"""
	Standard class for progamming {name}s.\n
	It requires {len(args)} {'argument' if len(args)<2 else 'arguments'}:
	{args_}
	```python
	{name.lower()} = {name}({arguments[0]})\n
	{name.lower()}.{method}({arguments[1]})\n
		{f'''wait(1)\n{name.lower()}.{method2}({arguments[2]})\n''' if method2 is not None else ''}
	"""
	return doc_string

name = input("Class name: ")
args = []

while True:
	a = input("Name: ")
	if a=="":
		break
	b = input("Type: ")
	c = input("Explanation: ")
	args.append(
			{
				"name":a,
				"type":b,
				"e":c
			}
		)

arguments = []

flag = False

a1 = input("Arguments for class: ")
a2 = input("Arguments for first method: ")
a3 = input("Arguments for last method('' if no last): ")

arguments.append(a1)
arguments.append(a2)
if a3 != "end123":
	arguments.append(a3)
else:
	flag = True

m1 = input("First method: ")
m2 = None
if not flag:
	m2 = input("Second method: ")

print(f'"""{make(name, args,arguments,m1,m2)}"""')