from a import *
from gen import *
from gen import Generator
a = Generator(Parser(Lexer("""
if 1==1:
	1+23""").evaluate()).parse().body)
v = VM(a.run())
print("DHFNHEUI", v.bytecode)
b=v.run()
print("RETURNED", b)