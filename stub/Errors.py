from warnings import warn
INSPIRE="""
    Remember, Errors are part of the process. Each one helps you understand your code better.
        Something went wrong — that's okay.
        Every error is a step toward a better program.😄"""
DOUBT="""
    If the traceback worried you, don't worry, it will lead you to the exact place the error happend. 
    If the traceback ends with line numbers that are not yours they are usually just raise statements in the module."""

ERROR_NUMS={
    "MicroControllerError": "0",

    "PinError": "0.0",
    "PinNotApplicableError": "0.0.0",
    "PinOutOfRangeError": "0.0.1",
    "InvalidPinTypeError": "0.0.2",
    "PinAlreadyInUseError": "0.0.3",

    "InvalidArgumentError": "0.1",

    "BoardError": "0.2",
    "BoardNotInitializedFirstError": "0.2.0",
    "BoardNotDefinedError": "0.2.1",

    "DeviceNotCompatibleWithCurrentBoardError":"0.3"

}
class ReservedPinWarning(UserWarning):
    pass
def reserved_pin_warn(pin,name):
    warn(
        f"Pin {pin} is a reserved pin({name}) in the microcontroller. It may cause Errors and problems in future. This is only a Warning. ",
        ReservedPinWarning
    )
    
class MicroControllerError(Exception):
    def __init__(self, message,hint=""):
        self.message,self.hint=message,hint
        super().__init__(message)
    def __str__(self):
        if self.hint:
            self.message="Error: "+self.message+"\n"+"Hint: "+self.hint
        return f"[Error number: {ERROR_NUMS[self.__class__.__name__]}]"+self.message+"\n"+"_"*90+INSPIRE+"\n"+"_"*90+DOUBT+"\n"+"_"*90
class PinError(MicroControllerError):
    pass
class PinNotApplicableError(PinError):
    def __init__(self, pin,pintype, needed):
        self.pin=pin
        self.pintype=pintype
        self.needed=needed
        self.message=f"An {pintype} pin({pin}) was used where {needed} was needed."
        self.hint=f"Use a {needed} pin for this device."
        super().__init__(self.message,self.hint)
class PinOutOfRangeError(PinError):
    def __init__(self, pin, current_board):
        self.pin=pin
        self.message=f"Pin {pin} was used when the valid pin range is {min(current_board.pinnames)}-{max(current_board.pinnames)}"
        super().__init__(self.message)
class InvalidPinTypeError(PinError):
    def __init__(self, pin, pins:list):
        self.pin=pin
        self.pins=pins
        self.message=f"Pinname {pin} is not a valid pinname"
        self.hint=f"Use only pinnames like {",".join(pins)}"
        super().__init__(self.message,self.hint)
class PinAlreadyInUseError(PinError):
    def __init__(self, pin):
        self.pin=pin
        self.message=f"Pin {pin} is already in use."
        self.hint=f"Use other pins for this device"
        super().__init__(self.message,self.hint)
class InvalidArgumentError(MicroControllerError):
    def __init__(self,argument,needed,obj="type"):
        self.argument=argument
        self.needed=needed
        self.message=f"Argument '{argument}' was used where an argument of {obj} {needed} was needed."
        self.hint=f"Use an argument of {obj} {needed} for this function."
        super().__init__(self.message,self.hint)
class BoardError(MicroControllerError):
    pass
class BoardNotInitializedFirstError(BoardError):
    def __init__(self):
        self.message=f"Please initialize the board before your code."
        self.hint=f"Use the 'set_board()' function to select your board."
        super().__init__(self.message,self.hint)
class BoardNotDefinedError(BoardError):
    def __init__(self, board):
        self.board=board
        self.message=f"Board {board} is not defined in the stub JSON file."
        self.hint=f"""Define a new board by making a class with the following syntax:
            class {board}(Board):
                def setup():
                    pins=[MCUpin.generate_array(Analog,Digital,map)]# use map to generate using your custom pins
                    board={board}()
                    board.export()
                """
        super().__init__(self.message,self.hint)
class DeviceNotCompatibleWithCurrentBoardError(MicroControllerError):
    def __init__(self,device,currentboard,reason):
        self.device=device
        self.reason=reason
        message=f"Device {device} is not compatible with the currentboard({currentboard}) because it doesnt have {reason}."
        hint=f"Either change the board to a compatible one or do not use the device."
        super().__init__(message, hint)

if __name__=="__main__":

    raise MicroControllerError("Test for evidence","Hint")
    