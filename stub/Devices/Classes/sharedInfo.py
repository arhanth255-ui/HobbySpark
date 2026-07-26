from ...Boards import Board,BoardDataManager,path
from ...Errors import *
import stub.Boards as Boards

debug=False
def board_check():
    if Boards.CURRENTBOARD==None:
        raise BoardNotInitializedFirstError()

def pin_value(pin:str|int,includemode=False):
    if isinstance(pin,int):
        if includemode:
            return str(pin),"digital"
        else:
            return str(pin)
    elif isinstance(pin,str):
        if pin.isdigit():
            if includemode:
                return pin,"digital"
            else:
                return pin
        elif (pin.upper().startswith("A")) and pin[1:].isdigit():
            if includemode:
                return pin.upper(),"analog"
            else:
                return pin[1:]
        elif pin == "SDA":
            if includemode:
                return pin_value(Boards.CURRENTBOARD.sda, True)
            else:
                return pin_value(Boards.CURRENTBOARD.sda)
        elif pin == "SCL":
            if includemode:
                return pin_value(Boards.CURRENTBOARD.scl, True)
            else:
                return pin_value(Boards.CURRENTBOARD.scl)
        elif pin == "LED":
            if includemode:
                return pin_value(Boards.CURRENTBOARD.onboard_led, True)
            else:
                return pin_value(Boards.CURRENTBOARD.onboard_led)
        else:
            raise InvalidPinTypeError(pin,pins_in_dic)
used_pins=[]
pins_in_dic=[]
modes_in_dic=[]
PWM_pins=[]
specialities_in_dic=[]
pins={}
pins_and_modes={}
pins_and_specialities={}


def startup():
    global pins_in_dic
    global modes_in_dic
    global specialities_in_dic
    global pins_and_modes
    global pins_and_specialities
    global PWM_pins
    global pins

    pins_in_dic.clear()
    modes_in_dic.clear()
    specialities_in_dic.clear()
    pins_and_modes.clear()
    pins_and_specialities.clear()
    PWM_pins.clear()
    pins.clear()
    pins_address:dict=Boards.CURRENTBOARD.pinmap
    PWM_pins.extend(Boards.CURRENTBOARD.PWMpins)
    pins={"analog":[],"digital":[]}
    for pin in pins_address.keys():
        pins_in_dic.append(pins_address[pin]["pinname"])
        modes_in_dic.append(pins_address[pin]["mode"])
        specialities_in_dic.append(pins_address[pin]["speciality"])

    for pin, mode in zip(pins_in_dic, modes_in_dic):
        pins_and_modes[pin] = mode

    for pin, special in zip(pins_in_dic, specialities_in_dic):
        pins_and_specialities[pin] = special
    
    for pin in pins_in_dic:
        pin,mode=pin_value(pin,True)
        pin=pin_value(pin)
        if mode=="analog":
            pins["analog"].append(int(pin))
        elif mode=="digital":
            pins["digital"].append(int(pin))




class   Pin():
    def __init__(self,pin:str|int,needed:str="both",speciality:str=None)->None:
        board_check()
        raw_pin,mode=pin_value(pin,True)
        pin=pin_value(pin)
        global used_pins
        if int(pin)>max(pins[mode]):
            raise PinOutOfRangeError(pin,Boards.CURRENTBOARD)
        if raw_pin in used_pins:
            raise PinAlreadyInUseError(raw_pin)
        if pins_and_specialities[raw_pin]!=speciality and speciality is not None:
            raise PinNotApplicableError(raw_pin,mode, speciality)
        if needed!="both":    
            if mode!=needed:                  
                raise PinNotApplicableError(raw_pin,mode,needed)
        for name, reserved_pin in Boards.CURRENTBOARD.reservedpins.items():
            if str(reserved_pin) == raw_pin:
                reserved_pin_warn(raw_pin,name)
                break
        used_pins.append(raw_pin)
        self.pinname=pin


def set_board(board:Board, debug_mode:bool = True):
    global debug
    if not isinstance(debug_mode,bool):
        raise InvalidArgumentError(debug_mode, "bool")
    elif not isinstance(board,Board):
        raise InvalidArgumentError(board,"Board","class")
    debug=debug_mode
    with open(path,"r") as file:
        boards=dict(BoardDataManager.load(file)).keys()
        if str(board) in list(boards):
            Boards.CURRENTBOARD=board
            Boards.CURRENTBOARD.export()
            startup()
        else:
            board.export()
            set_board(board)


        