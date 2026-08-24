from a import *
from gen import *
from gen import Generator
a = Generator(Parser(Lexer("""
a = 0
b = a
c = b<7
a
call(b,c)""").evaluate()).parse().body)
v = VM(a.run())
print("DHFNHEUI", v.bytecode)
b=v.run()
print("RETURNED", b)