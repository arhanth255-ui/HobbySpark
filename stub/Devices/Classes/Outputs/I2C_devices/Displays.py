from ....Constants import *
from ....Functions import *
from .....Boards import *
from .....Errors import *
from inspect import currentframe as currentframe
from ...sharedInfo import Pin

class I2C_LCD_Display:
	"""Standard class for programming **displays**.\n
    It requires 5 arguments:\n
        1. sda - an int or string - the sd pin.\n
        2. scl - an int or string -  the scl pin.\n
        3. width - an int - the display width. \n
        4. height - an int -  the display height.\n
        5. address - an memory address or string - the I2C address the display is located at.
    You can use it using the following syntax:\n
    ```python
        dis=I2C_LCD_Display("SDA","SCL", 16, 2, 0x24)
        dis.set_cursor(0,0)
        dis.write("Hello world!")"""
	meta={
            "pin_args":{
                "0":"sda",
                "1":"scl"
            },
            "requires_updt":True,
        	"requires_even":False
    }
	def __init__(self, sda, scl, width, height, address) -> None:
		self.sda = Pin(sda, speciality="sda")
		self.scl = Pin(scl, speciality="scl")
		self.width = width
		self.height = height

	def set_cursor(self,x, y):
		"""Sets the cursor position on the I2C LCD display to the specified column and row."""
		if not isinstance(x, int) or x>self.width:
			raise InvalidArgumentError(x, "int lesser than screen width. ")

		if not isinstance(y, int) or y>self.height:
			raise InvalidArgumentError(y, "int lesser than screen height. ")

		check(self,currentframe().f_code,locals())

	def write(self, string):
		"""Writes the given string to the display."""
		check(self,currentframe().f_code,locals())

	def scroll_text(self, string, delay, unit = MS):
		"""Scrolls the given string across the display with a specified delay and duration."""
		check(self,currentframe().f_code,locals())

	def scroll_with_millis(self, start_string, delay, unit = MS):
		"""Scrolls the given text across the display with the specified delay. It is non interrupting and array based. You can add upto 80 messsages.
		Use the add method to add messages."""
		
		check(self,currentframe().f_code,locals())

	def add(self, string, importance=0):
		"""Adds a string to the scroll array. Call scroll_with_millis before calling this.\n
		The importance can be an int between 0 and 2.\n
		* importance of 0 bypasses all currently scrolling messages.\n
		* importance of 1 appears directly after the current message.\n
		* importance of 2 adds the message to the stack, appearing after all messages in the stack finish scrolling. """
		if not isinstance(importance, int) or importance>2:
			raise InvalidArgumentError(importance, "int between 0 and 2")
		check(self,currentframe().f_code,locals())
		

