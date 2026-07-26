import lexer
import parser as p
import transpiler as t
from pathlib import Path
print("""Python 3.13.13 (tags//v3.13.13:01104ce, Apr  7 2026, 19:25:48) [MSC v.1944 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "lbicense" for more information.""")

a=False
while a:
   a=lexer.Lexer(input(">>> "))
   b=a.evaluate()
   print(b)
   c=p.Parser(b)
   ab=c.parse()
   tr = t.Transpiler(ab)
   print("\n".join(tr.translate()))
a="zxyyyyyyyyy.py" 
b="transpiler_new.py"
with open(a) as f:
    q=f.read()
    f=lexer.Lexer(q)
    l=f.evaluate()
    print(l)
    print(l)
    a=p.Parser(l)
    ab=a.parse()
    print(ab)
    tr = t.Transpiler(ab)
    print("\n".join(tr.translate()))

