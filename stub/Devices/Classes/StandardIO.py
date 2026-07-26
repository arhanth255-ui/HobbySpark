from ..Constants import *
from ..Functions import *
from ...Boards import *
from ...Errors import *
from inspect import currentframe
from typing import Any
from .sharedInfo import Pin
import stub.Boards as boarddata

class Analog:
    """Standard class for programming analog pins and devices which require them.\n
    Why is it here?
    Ans:Well, though I've implemented as much devices as possible, some devices might not be supported.
    Therefore, I've created 2 classes for programming individual pins-Analog and Digital. 
    It requires 1 argument:\n
        1. pin - an int or string - the pin from which all methods write data to.\n
    You can use it using the following syntax:\n
        pin=Analog(1)\n
        pin.write(12)\n
        wait(1000,MS)\n
        reading=pin.read()"""
    meta={
            "pin_args":{
                "0":"pin"
            },
            "requires_updt":False,
            "requires_even":False
        }
    def __init__(self,pin)->None:
        self.pin=Pin(pin,"analog")
        
    def write(self,value)->None:
        """Writes an value(in percentage) to the given pin."""
        check(self,currentframe().f_code,locals())
    def read(self)->int:
        """Reads an value on the given pin and returns it(in percentage)."""
        check(self,currentframe().f_code,locals())


class Digital:
    """Standard class for programming digital pins and devices which require them.\n
    Why is it here?
    Ans:Well, though I've implemented as much devices as possible, some devices might not be supported.
    Therefore, I've created 2 classes for programming individual pins-Analog and Digital. 
    It requires 1 argument:\n
        1. pin - an int or string - the pin from which all methods write data to.\n
    You can use it using the following syntax:\n
        pin=Digital(1)\n
        pin.write(True)\n
        wait(1000,MS)\n
        reading=pin.read()
        """
    meta={
            "pin_args":{
                "0":"pin"
            },
            "requires_updt":False,
            "requires_even":False
        }
    def __init__(self,pin):
        self.pin=Pin(pin)
        
    def write(self,value):
        """Writes an value(as bool) to the given pin."""
        check(self,currentframe().f_code,locals())
    def read(self)->bool:
        """Reads an value on the given pin and returns it(as bool)."""
        check(self,currentframe().f_code,locals())


class SerialMoniter():
    """Standard class for communication with to the computer from a microcontroller.\n
    It requires 1 argument:\n
        1. baud - an int - the baudrate from which the communictaion should take place.\n
    You can use it using the following syntax:\n
        serial=Serial(9600)\n
        serial.print("Hello world!, from the microcontroller)\n
        serial.input() """
    meta={
            "pin_args":{
            },
            "requires_updt":False,
            "requires_even":False
    }
    def __init__(self,baud:int=9600)->None:
        if isinstance(baud,int):
            self.baudrate=baud
        else:
            raise InvalidArgumentError(baud,"int")
        
    def print(self,string:Any)->None:
        """Prints the given arg(string) to the serial moniter."""
        if not isinstance(string,(str,int,float)):
            raise InvalidArgumentError(string,"str,int or float")
        check(self,currentframe().f_code,locals())

    def input(self)->str:
        """Takes input from the serial moniter, returning a string."""
        check(self,currentframe().f_code,locals())

    def available(self):
        """Returns a bool, telling whether an input is available or not. """
        check(self,currentframe().f_code,locals())


class EEPROM:
    meta={
            "pin_args":{
            },
            "requires_updt":False,
            "requires_even":False
    }
    def __init__(self,memory:dict[str:int]={}):
        if not boarddata.CURRENTBOARD.has_EEPROM:
            raise DeviceNotCompatibleWithCurrentBoardError("EEPROM",boarddata.CURRENTBOARD,"EEPROM")
        self.memory=memory
    def read(self,address_or_string):
        if isinstance(address_or_string,int):
            if address_or_string not in self.memory:
                raise InvalidArgumentError(address_or_string,"valid string or int(address name)")
        elif isinstance(address_or_string,str):
            if address_or_string not in self.memory.values():
                raise InvalidArgumentError(address_or_string,"valid string or int(address name)")
        else:
            raise InvalidArgumentError(address_or_string,"valid string address name or int")
        check(self,currentframe().f_code,locals())
        return self.memory[address_or_string]
    def write(self,address_or_string,value):
        if not isinstance(address_or_string,(int,str)):
            raise InvalidArgumentError(address_or_string,"valid string address name or int")
        self.memory[address_or_string]=value
        check(self,currentframe().f_code,locals())
    def update(self,address_or_string,value):
        if not isinstance(address_or_string,(int,str)):
            raise InvalidArgumentError(address_or_string,"valid string address name or int")
        if self.memory.get(address_or_string)==value:
            pass
        else:
            self.memory[address_or_string]=value
        check(self,currentframe().f_code,locals())
    def delete(self,address_or_string):
        if not isinstance(address_or_string,(int,str)) or self.memory.get(address_or_string) is None:
            raise InvalidArgumentError(address_or_string,"valid string address name or int")
        self.memory[address_or_string]=None
        check(self,currentframe().f_code,locals())
    

class Wifi:
    meta={
            "pin_args":{
            },
            "requires_updt":False,
            "requires_even":False
    }
    def connect(self, wifi_name, wifi_password):
        if not isinstance(wifi_name,str):
            raise InvalidArgumentError(wifi_name, "str")
        if not isinstance(wifi_password,str):
            raise InvalidArgumentError(wifi_password, "str")
        check(self,currentframe().f_code,locals())

    def disconnect(self):
        check(self,currentframe().f_code,locals())

    def is_connected(self):
        check(self,currentframe().f_code,locals())

    def get_ip(self):
        check(self,currentframe().f_code,locals())

    def mac(self):
        check(self,currentframe().f_code,locals())

    def signal(self):
        check(self,currentframe().f_code,locals())

    def scan(self):
        check(self,currentframe().f_code, locals())

class Http:
    meta={
            "pin_args":{
            },
            "requires_updt":False,
            "requires_even":False
    }
    def get(self, url):
        if not isinstance(url,str):
            raise InvalidArgumentError(url, "str")
        check(self,currentframe().f_code,locals())

    def post(self,url, data):
        if not isinstance(url,str):
            raise InvalidArgumentError(url, "str")
        check(self,currentframe().f_code,locals())