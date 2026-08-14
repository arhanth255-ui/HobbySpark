from ...Constants import *
from ...Functions import *
from ....Boards import *
from ....Errors import *
from inspect import currentframe
from ..sharedInfo import Pin,PWM_pins

class RGB:
    def __init__(self,r,g,b) -> None:
        self.r=r
        self.b = b
        self.g = g

    def hash(self):
        """Returns the color as a hash. """

class Led:
    """
                Standard class for progamming Leds.

                It requires 1 argument:
                1. pin - An int or string - The pin all methods write to.

                ```python
                led = Led('4')

                led.on()

                wait(1)
                led.off()
"""
    meta={
            "pin_args":{
                "0":"pin"
            },
            "requires_updt":True,
            "requires_even":False
        }
    def __init__(self,pin)->None:
        self.pin=Pin(pin,"both")
        

    def on(self)->None:
        """Turns on the led connected to pin."""
        check(self,currentframe().f_code,locals())
        
    def off(self)->None:
        """Turns off the led connected to pin."""
        check(self,currentframe().f_code,locals())

    def blink(self,speed,unit=MS,times=None)->None:
        """Blinks the led connected to pin speed arg(times) times, waiting arg(speed) before each blink with the unit of time as arg(times)."""
        if not isinstance(speed,(int,float)):
            raise InvalidArgumentError(speed,"int or float")
        if not isinstance(unit,int):
            raise InvalidArgumentError(unit,"constant int or int")
        if not isinstance(times,int):
            raise InvalidArgumentError(times,"int")
        check(self,currentframe().f_code,locals())

    def set_brightness(self,PWM_output)->None:
        """Sets the brightness of the led connected to pin to arg(PWM_output)(in percent, not 0 to 255)."""
        if not isinstance(PWM_output,int) or not 100<PWM_output>0:
            raise InvalidArgumentError(PWM_output,"int between 0 and 100")
        if not self.pin.pinname in PWM_pins:
            raise PinNotApplicableError(self.pin.pinname, "non PWM", "PWM")
        check(self,currentframe().f_code,locals())

    def fade(self,time,unit=MS)->None:
        """Fades the led connected to pin for arg(time) with the unit as arg(unit)."""
        if not isinstance(time,(int,float)):
            raise InvalidArgumentError(time,"int or float")
        if not isinstance(unit,(int,float)):
            raise InvalidArgumentError(unit,"int or float")
        if not self.pin.pinname in PWM_pins:
            raise PinNotApplicableError(self.pin.pinname, "non PWM", "PWM")
        check(self,currentframe().f_code,locals())

    def toggle(self)->None:
        """Puts the led on pin to the opposite state of now."""
        check(self,currentframe().f_code,locals())

    def returnState(self)->tuple[bool,int]:
        """Returns the state of the led connected to pin as bool with True as on as tuple with format (state,pwm)."""
        check(self,currentframe().f_code,locals())


class RGBled:
    """Standard class for programming RGB leds.\n
    It requires 3 argument:\n
        1. r - an int or string - the pin to which you have connected the r pin of the led to.\n
        2. g - an int or string - the pin to which you have connected the g pin of the led to.\n
        3. b - an int or string - the pin to which you have connected the b pin of the led to.\n
    You can use it using the following syntax:\n
    ```python
        led=RGBled(1)\n
        led.set(100,100,100)\n
        wait(1000,MS)\n
        led.off()"""
    meta={
            "pin_args":{
                "0":"r",
                "1":"g",
                "2":"b"
            },
            "requires_updt":True,
            "requires_even":False
        }
    def __init__(self,r,g,b)->None:
        self.r=Pin(r,"both")
        self.g=Pin(g,"both")
        self.b=Pin(b,"both")
        
    def set(self,r,g,b)->None:
        """Sets the led to the values given in r, g and b(values in percentage)."""
        if not isinstance(r,int) and not 100<r>0:
            raise InvalidArgumentError(r,"int between 0 and 100")
        if not isinstance(g,int) and not 100<g>0:
            raise InvalidArgumentError(g,"int between 0 and 100")
        if not isinstance(b,int) and not 100<b>0:
            raise InvalidArgumentError(b,"int between 0 and 100")
        check(self,currentframe().f_code,locals())
        
    def off(self)->None:
        """Turns the led off by setting it to 0,0,0."""
        check(self,currentframe().f_code,locals())
        
    def fade(self,r,g,b,time,unit)->None:
        """Fades the led with the given values for arg(time) with the unit as arg(unit)."""
        if not isinstance(time,(int,float)):
            raise InvalidArgumentError(time,"int or float")
        if not isinstance(unit,int):
            raise InvalidArgumentError(unit,"int")
        if not isinstance(r,int) and not 100<r>0:
            raise InvalidArgumentError(r,"int between 0 and 100")
        if not isinstance(g,int) and not 100<g>0:
            raise InvalidArgumentError(g,"int between 0 and 100")
        if not isinstance(b,int) and not 100<b>0:
            raise InvalidArgumentError(b,"int between 0 and 100")
        check(self,currentframe().f_code,locals())
        
    def return_state(self)->tuple[int]:
        """Returns the state of the led as a RGB class(all values as percentage)."""
        check(self,currentframe().f_code,locals())
        
    def blink(self,r,g,b,times,speed,unit)->None:
        """Blinks the led with the given values speed arg(times) times, waiting arg(speed) before each blink with the unit of time as arg(times)."""
        if not isinstance(r,int) and not 100<r>0:
            raise InvalidArgumentError(r,"int between 0 and 100")
        if not isinstance(g,int) and not 100<g>0:
            raise InvalidArgumentError(g,"int between 0 and 100")
        if not isinstance(b,int) and not 100<b>0:
            raise InvalidArgumentError(b,"int between 0 and 100")
        check(self,currentframe().f_code,locals())
    def set_color(self,color=RED)->None:
        """Sets the led to the color given."""
        check(self,currentframe().f_code,locals())



