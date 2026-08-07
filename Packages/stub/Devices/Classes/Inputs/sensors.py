from ...Constants import *
from ...Functions import *
from ....Boards import *
from ....Errors import *
from inspect import currentframe
from ..sharedInfo import Pin
class UltrasonicSensor:
    """Standard class for programming ultrasonic sensors.\n
    It requires  argument:\n
        1. trig - an int or string - the pin to which you have connected the trig pin to.\n
        1. echo- an int or string - the pin to which you have connected the echo pin to.\n
    You can use it using the following syntax:\n
    ```python
        sensor=UltrasonicSensor(1)\n
        serial=Serial(9600)
        serial.print(sensor.distance()+"cm")\n"""

    meta={
            "pin_args":{
                "0":"echo",
                "1":"trig"
            },
            "requires_updt":False,
            "requires_even":True,
            "big":True,
            "methods":{
                "when_distance":{"arg":0, "i":1}
            }
        }
    def __init__(self,echo,trig)->None:
        self.echopin=Pin(echo)
        self.trigpin=Pin(trig)
        
    
    def distance(self)->int:
        """Returns the distance in between the sensor and an object in cm."""
        check(self,currentframe().f_code,locals())

    def when_distance(self, distance, function):
        """Executes function when the sensor.distance is distance. """
        check(self,currentframe().f_code,locals())
