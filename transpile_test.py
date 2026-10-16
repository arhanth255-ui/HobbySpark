from parser import *
from nodes import *
from lexer import *
from semantic_analyzer import *
from json import dumps, loads

input = """
b = 12+0.132
c = b+12
d = c
"""

lexed = Lexer(input).evaluate()

parsed = Parser(lexed).parse()

nodes = SemanticAnalyzer(parsed).analyze_semantically()

a=[dumps(a[1], indent=4) for a in nodes]

for b in a: print(b)

print("Remember,",repr(Types.INT), repr(Types.FLOAT), repr(Types.STRING), repr(Types.BOOL), repr(Types.UNKNOWN))
print()

print([a[0] for a in nodes])
