"""from ...Constants import *
from ...Functions import *
from ....Boards import *
from ....Errors import *
from inspect import currentframe as currentframe
from ..sharedInfo import Pin

class Transistor:
	def __init__(self, pin) -> None:
		self.pin = Pin(pin)

	def on(self):
		check(self, currentframe().f_code, locals())

	def off(self):
		check(self, currentframe().f_code, locals())

	def write_value(self, value:int):
		if not isinstance(value, int) or 0>value>100:
			raise InvalidArgumentError(value, "an int between 1 and 100")

		if self.pin.pinname not in CURRENTBOARD.PWMpins:
			raise PinNotApplicableError(self.pin.pinname, "non PWM", "PWM")
		"""