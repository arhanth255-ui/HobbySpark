from ...Constants import *
from ...Functions import *
from ....Boards import *
from ....Errors import *
from inspect import currentframe
from ..sharedInfo import Pin

class ServoMotor:
	"""Standard class for programming servos.\n
    It requires 1 argument:\n
        1. pin - an int or string - the pin from which all methods write data to.\n
    You can use it using the following syntax:\n
    ```python
        servo=Servo(1)\n
        servo.write(12)\n
	"""
	meta={
            "pin_args":{
                "0":"pin"
            },
            "requires_updt":True,
        	"requires_even":False
    	}
	def __init__(self, pin) -> None:
		self.pin = Pin(pin)

	def write(self, degrees):
		"""
		Sets the servo to degrees.
		"""
		if not isinstance(degrees, int) or 0<degrees>180:
			raise InvalidArgumentError(degrees, "int between 0 and 180")

		check(self,currentframe().f_code,locals())

	def move_smooth(self, degrees, speed, unit = MS):
		"""Moves the servo steadily towards degrees inside of speed."""
		if not isinstance(degrees, int) or 0<degrees>180:
			raise InvalidArgumentError(degrees, "int between 0 and 180")

		if not isinstance(speed, (int,float)):
			raise InvalidArgumentError(speed, "int or float")

		check(self,currentframe().f_code,locals())

	def return_state(self):
		"""Returns the servo's state as an integer. """
		check(self, currentframe().f_code, locals())


def check_I2C_devices():
	"""Checks for all I2C devices and prints them to the serial moniter at baud rate 9600."""
	pass
