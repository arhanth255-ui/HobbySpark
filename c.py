from a import *
from gen import *
from gen import Generator
a = Generator(Parser(Lexer("""
a = 0
b = 0
c = b<7
while c:
	b = b+1
	
	if a==12:
		continue
	a = a+3
a""").evaluate()).parse().body)
v = VM(a.run())
print("DHFNHEUI", v.bytecode)
b=v.run()
print("RETURNED", b)