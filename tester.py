from vm import *
from gen import *
from gen import Generator
a = Generator(Parser(Lexer("""
def call(a,b=98):
	bn = a+b
	print(bn)
	return bn
b=12
c=14
d=call(b)+1
print(d)
""").evaluate()).parse().body)
x,y=a.run()
v = VM(x, y)
print("DHFNHEUI", v.bytecode, "\n", y[0].bytecode)
c=v.run()
print("RETURNED", c)