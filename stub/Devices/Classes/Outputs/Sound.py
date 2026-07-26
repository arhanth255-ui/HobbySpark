from ...Constants import *
from ...Functions import *
from ....Boards import *
from ....Errors import *
from inspect import currentframe
from ..sharedInfo import Pin, PWM_pins

class ActiveBuzzer:
	"""Standard class for programming active buzzers.\n
    It requires 1 argument:\n
        1. pin - an int or string - the pin from which all methods write data to.\n
    You can use it using the following syntax:\n
    ```python
        buzzer=Buzzer(1)\n
        buzzer.on()\n
        wait(1000,MS)\n
        buzzer.off()"""
	meta={
            "pin_args":{
                "0":"pin"
            },
            "requires_updt":False,
            "requires_even":False
        }
	def __init__(self, pin) -> None:
		self.pin = Pin(pin)

	def on(self):
		"""Turns the buzzer on."""
		check(self,currentframe().f_code,locals())

	def off(self):
		"""Turns the buzzer off."""
		check(self,currentframe().f_code,locals())

	def toggle(self):
		"""Toggles the buzzer."""
		check(self,currentframe().f_code,locals())

	def returnstate(self):
		"""Returns the state as a boolean."""
		check(self,currentframe().f_code,locals())

class PassiveBuzzer:
	"""Standard class for programming passive buzzers.\n
    It requires 1 argument:\n
        1. pin - an int or string - the pin from which all methods write data to.\n
    You can use it using the following syntax:\n
    ```python
        buzzer=Buzzer(1)\n
        buzzer.on()\n
        wait(1000,MS)\n
        buzzer.off()"""
	meta={
            "pin_args":{
                "0":"pin"
            },
            "requires_updt":False,
            "requires_even":False
        }
	def __init__(self, pin) -> None:
		self.pin = Pin(pin)
		if not self.pin.pinname in PWM_pins:
			raise PinNotApplicableError(pin, "non PWM", "PWM")

	def write(self, frequency, time = 1, unit = SEC):
		"""Puts the buzzer to the given frequency. """
		check(self,currentframe().f_code,locals())

	def write_note(self, note=REST, time=1, unit =SEC):
		"""Puts the buzzer to the note."""
		check(self,currentframe().f_code,locals())

	def pause(self, time=1, unit = SEC):
		"""Pauses the buzzer. """
		check(self,currentframe().f_code,locals())

	def returnstate(self):
		"""Returns the state as a float. """
		check(self,currentframe().f_code,locals())