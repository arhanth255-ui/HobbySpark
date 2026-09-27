from stub import *
from nodes import *
print([a for a in globals() if a.endswith("Node")])
set_board(ArduinoNanoEvery(), True)
Led(12)



