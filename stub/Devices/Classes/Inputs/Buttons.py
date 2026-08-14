from ...Constants import *
from ...Functions import *
from ....Boards import *
from ....Errors import *
from inspect import currentframe
from ..sharedInfo import Pin


class Button:
    """Standard class for programming buttons.\n
    It requires 1 argument:\n
        1. pin - an int or string - the pin from which all methods read data from.\n
    You can use it using the following syntax:\n
    ```python
        button=Button(1)\n
        reading=button.read()
       """
    meta={
            "pin_args":{
                "0":"pin"
            },
            "requires_updt":False,
            "requires_even":True,
            "big":False,
            "methods":{
                "when_read":{"arg":None, "i":0}
            }
        }
    def __init__(self,pin)->None:
        self.buttonpin=Pin(pin)
        
    def read(self)->bool:
        """Returns the button state as a bool. Note: button.read returns the state at the exact moment the line terminates."""
        check(self,currentframe().f_code,locals())
    def when_read(self, func)->bool:
        """Returns the button state as a bool and runs the function given whenever True. Note: button.whenread(func) returns the state at the exact moment the line terminates but runs the function while the microcontroller is active and button.read is True."""
        check(self,currentframe().f_code,locals())


class Potentiometer:
    """Standard class for programming potentiometers.\n
    It requires 1 argument:\n
        1. middle_pin - an int or string - the pin to which you have connected the middle pin of the pot to.\n
    You can use it using the following syntax:\n
    ```python
        pot=Potentiometer(7)
        a=pot.read()"""
    meta={
            "pin_args":{
                "0":"middle_pin"
            },
            "requires_updt":False,
            "requires_even":True,
            "big":True,
            "methods":{
                "when_read":{"arg":1, "i":0}
            }
        }
    def __init__(self,middle_pin):
        self.pot_pin=Pin(middle_pin,"analog")
        
    def read(self)->int:
        """Returns the pot state as percentage. Note: pot.read returns the state at the exact moment the line terminates."""
        check(self,currentframe().f_code,locals())
    def read_raw(self)->int:
        """Returns the pot state as an int from 0 to 1023. Note: pot.read returns the state at the exact moment the line terminates."""
        check(self,currentframe().f_code,locals())
    def when_read(self,func,reading=0)->int:
        """Returns the pot state as a bool and runs the function given whenever reading is the given value. Note: pot.whenread(func) returns the state at the exact moment the line terminates but runs the function while the microcontroller is active and button.read is True."""
        check(self,currentframe().f_code,locals())
