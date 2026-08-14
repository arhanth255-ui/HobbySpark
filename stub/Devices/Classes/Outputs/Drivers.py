from ...Constants import *
from ...Functions import *
from ....Boards import *
from ....Errors import *
from inspect import currentframe as currentframe
from ..sharedInfo import Pin

class Driver():
    """Standard class for programming drivers.\n
    It requires 2-3 argument:\n
        1. in1- an int or string - the pin connected to the IN1 pin on the driver.\n
        2. in2- an int or string - the pin connected to the IN2 pin on the driver.\n
        3. enable - an int or string - the pin connected to the enable pin on the driver.\n
    Remember, the enable pin should be an analog one.\n
    Without the enable pin connected, the motor will always stay at 100 percent speed. Use enable when you want speed control. 
    You can use it using the following syntax:\n
    ```python
        motor=Driver(7,8,A1)\n
        motor.forward(12,MS)
        """
    meta={
            "pin_args":{
                "0":"in1",
                "1":"in2",
                "2":"enable"
            },
            "requires_updt":False,
            "requires_even":False
        }
    def __init__(self,in1,in2,enable=None)->None:
        self.in1=Pin(in1)
        self.in2=Pin(in2)
        self.enable=Pin(enable,"analog")
        

    def forward(self,duration,unit=MS,intensity=-1)->None:
        """Sets the motor to go forward for arg(duration) with intensity arg(intensity) and unit arg(unit)."""
        if not isinstance(duration,(int,float)):
            raise InvalidArgumentError(duration,"int or float")
        if not isinstance(unit,int):
            raise InvalidArgumentError(unit,"int")
        if not isinstance(intensity, int) or not (0 <= intensity <= 100):
            raise InvalidArgumentError(unit,"int between 0 and 100","an")
        check(self,currentframe().f_code,locals())
    
    def backward(self,duration,unit=MS,intensity=-1)->None:
        """Sets the motor to go backward for arg(duration) with intensity arg(intensity) and unit arg(unit)."""
        if not isinstance(duration,(int,float)):
            raise InvalidArgumentError(duration,"int or float")
        if not isinstance(unit,int):
            raise InvalidArgumentError(unit,"int")
        if not isinstance(intensity, int) or not (0 <= intensity <= 100):
            raise InvalidArgumentError(unit,"int")
        check(self,currentframe().f_code,locals())
    
    def fadestop(self,time,unit=MS)->None:
        """Slowly stops the motor, making sure stopping it in arg(time) with unit arg(unit)."""
        if not isinstance(time,(int,float)):
            raise InvalidArgumentError(time,"int or float")
        if not isinstance(unit,int):
            raise InvalidArgumentError(unit,"int")
        check(self,currentframe().f_code,locals())
    
    def stop(self)->None:
        """Fully stops the motor with no delay."""
        check(self,currentframe().f_code,locals())



class TwoWheeledDriver:
    meta={
            "pin_args":{
                "0":"in1",
                "1":"in2",
                "2":"in3",
                "3":"in4",
                "4":"enable1",
                "5":"enable2"
            },
            "requires_updt":False,
            "requires_even":False
        }
    def __init__(self,in1,in2,in3,in4,enable1=None,enable2=None):
        self.motor1=Driver(in1,in2,enable1)
        self.motor2=Driver(in3,in4,enable2)
        self.enable1=Pin(enable1,"analog")
        self.enable2=Pin(enable2,"analog")
        

    def forward(self,duration,unit=MS,intensity=-1)->None:
        """Sets the motor to go forward for arg(duration) with intensity arg(intensity) and unit arg(unit)."""
        self.motor1.forward(duration, unit, intensity)
        self.motor2.forward(duration, unit, intensity)
        check(self,currentframe().f_code,locals())
    
    def backward(self,duration,unit=MS,intensity=-1)->None:
        """Sets the motor to go backward for arg(duration) with intensity arg(intensity) and unit arg(unit)."""
        self.motor1.backward(duration, unit, intensity)
        self.motor2.backward(duration, unit, intensity)
        check(self,currentframe().f_code,locals())
    
    def fadestop(self,time,unit=MS)->None:
        """Slowly stops the motor, making sure stopping it in arg(time) with unit arg(unit)."""
        self.motor1.fadestop(time,unit)
        self.motor2.fadestop(time,unit)
        check(self,currentframe().f_code,locals())
    
    def stop(self)->None:
        """Fully stops the motor with no delay."""
        check(self,currentframe().f_code,locals())

    def write(self,motor1,motor2,enable1,enable2,time,unit=MS):
        """Writes the motors to given values for the given time."""
        if not isinstance(motor1, bool):
            raise InvalidArgumentError(motor1, "bool")
        if not isinstance(motor2, bool):
            raise InvalidArgumentError(motor2, "bool")

        if not isinstance(enable1, int) or not (0 <= enable1 <= 100):
            raise InvalidArgumentError(enable1, "int between 0 and 100", "an")
        if not isinstance(enable2, int) or not (0 <= enable2 <= 100):
            raise InvalidArgumentError(enable2, "int between 0 and 100", "an")

        if not isinstance(time,(int,float)):
            raise InvalidArgumentError(time,"int or float")

        if not isinstance(unit,int):
            raise InvalidArgumentError(unit,"int")      

        check(self,currentframe().f_code,locals())
    def turn(self,direction,force,time,unit=MS):
        """Turns the motor with the given values."""
        if direction not in (LEFT, SLIGHT_LEFT, RIGHT, SLIGHT_RIGHT):
            raise InvalidArgumentError(direction, "a prebuilt constant")
        if not isinstance(force, int) or not (0 <= force <= 100):
            raise InvalidArgumentError(force, "int between 0 and 100", "an")

        if not isinstance(time,(int,float)):
            raise InvalidArgumentError(time,"int or float")

        if not isinstance(unit,int):
            raise InvalidArgumentError(unit,"int")   

        check(self,currentframe().f_code,locals())
        

    