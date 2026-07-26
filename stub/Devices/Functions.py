#imports
from ..Boards import *
from ..Errors import InvalidArgumentError,BoardNotInitializedFirstError
from .Constants import MS,SEC,US
import stub.Devices.Classes.sharedInfo as debug_var
def board_check():
    if CURRENTBOARD==None:
        raise BoardNotInitializedFirstError()

def check(self,function,args:dict):
    if debug_var.debug==False:
        return 
    variable_and_arg=[]
    for argname,argvalue in args.items():
        if argname=="self":
            continue
        elif argname=="unit" and argvalue in (SEC,MS,US):
            if argvalue==SEC:
                variable_and_arg.append(f"{argname}={f"second\\seconds({argvalue})"}")
                continue
            if argvalue==MS:
                variable_and_arg.append(f"{argname}={f"millisecond\\milliseconds({argvalue})"}")
                continue
            if argvalue==US:
                variable_and_arg.append(f"{argname}={f"microsecond\\microseconds({argvalue})"}")
                continue
        variable_and_arg.append(f"{argname}={argvalue}")
    
    print(f"Device: {self.__class__.__name__} has run {function.co_name}({", ".join(variable_and_arg)})")

def wait(time,unit=MS)->None:
    """Waits the for the given time in given unit. Button reads, pot reads etc run during the wait time."""
    if not isinstance(time,(int,float)):
        raise InvalidArgumentError(time,"int or float")
    if not isinstance(unit,int):
        raise InvalidArgumentError(unit,"int")

def interrupt(time,unit=MS)->None:
    """Completely blocks the microcontroller for doing anything for the given time."""
    if not isinstance(time,(int,float)):
        raise InvalidArgumentError(time,"int or float")
    if not isinstance(unit,int):
        raise InvalidArgumentError(unit,"int")