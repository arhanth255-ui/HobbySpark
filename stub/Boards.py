import json as BoardDataManager
from pathlib import Path
from .Errors import InvalidArgumentError,MicroControllerError
from platformdirs import user_config_dir

path=Path(user_config_dir("HobbySpark transpiler", appauthor=False, roaming=True))/"BoardsData.json"
folder=Path(user_config_dir("HobbySpark transpiler", appauthor=False, roaming=True))
folder.mkdir(parents=True, exist_ok=True)
if not path.exists() or path.stat().st_size == 0:
    with open(path, "w") as file:
       BoardDataManager.dump({}, file)


class MCUpin:
    def __init__(self,pinname,actualpin=None,mode="digital"):
        if isinstance(pinname,str):
            self.pinname=pinname
        else:
            raise InvalidArgumentError(pinname,"str")
        
        if isinstance(actualpin,str) or actualpin==None:
            self.actualpin=actualpin if actualpin != None else pinname
        else:
            raise InvalidArgumentError(pinname,"str")
        if mode=="digital" or mode=="analog":
            self.mode=mode
        else:
            raise InvalidArgumentError(pinname,"analog or digital",obj="type str")
        self.actualpin=actualpin if actualpin != None else pinname
    def __str__(self):
        return self.pinname
        
    def to_dict(self,PWM=True,speciality=None):
        data={self.pinname:{"pinname":self.pinname,"actualpin":self.actualpin,"mode":self.mode,"speciality":speciality,"PWM":PWM}}
        return data
    @staticmethod
    def generate_pin_array(Analog,Digital,map:dict=None):
        pins=[]
        for pin in range(Digital):
            if map==None:
                pins.append(MCUpin(str(pin),str(pin),"digital"))
            else:
                pins.append(MCUpin(map[str(pin)],map[str(pin)],"digital"))
        for pin in range(Analog):
            if map==None:
                pins.append(MCUpin("A"+str(pin),"A"+str(pin),"analog"))
            else:
                pins.append(MCUpin(map[str(pin)],map[str(pin)],"analog"))
        return pins

class Board:
    def __init__(self):
        self.boardname=None
        self.pinmap={}
        self.pins: list[MCUpin] = []
        self.sda=None
        self.scl=None
        self.onboard_led=None
        self.non_PWM_pins=[]
        self.has_wifi=False
        self.has_bluetooth=False
        self.has_EEPROM=False
        self.non_pwm_pinno=0
        self.TX=0
        self.RX=1
        self.reservedpins={"TX":0,"RX":1}
        self.setup()
        self.pinnames:list[int]=[p.pinname for p in self.pins]
        if not self.boardname:
            self.boardname=self.__class__.__name__
        self.PWMpins=[]
        for pin in self.pinnames:
            if self.non_pwm_pinno>=len(self.pins):
                self.PWMpins=["No pins"]
            elif pin not in self.non_PWM_pins:
                self.PWMpins.append(pin)
            else:
                self.non_pwm_pinno+=1
                continue
        if self.reservedpins.get("RX",None)==None or self.reservedpins.get("TX",None)==None:
            raise InvalidArgumentError(self.reservedpins,"a dictionary with keys RX and TX","")
        self.to_dict()
    def setup(self):
        """Overide setup by declaring the following:

            self.pins=[use MCUpin.generate_pin_array()]

            self.sda=sdapin(as MCUpin)

            self.scl=sclpin(as MCUpin)

            self.onboard_led=onboardled pin

            self.nonPWM_pins=[pins that arent pwm]

            self.has_wifi=bool

            self.has_bluetooth=bool

            self.RX=rxpin

            self.TX=txpin

            self.reserved_pins={"TX":tx,"RX":rx}

            self.has_EEPROM=bool

        or:

        self.set_variables()

            """
        
        print("You have defined nothing as boarddata.")
        print(self.setup.__doc__)
        raise MicroControllerError("Did not define setup().", "Define setup() in the custom board.")
    
    def to_dict(self):
        dic={}
        extra_reservedpins={}
        for name,reservedpin in self.reservedpins.items():
            if name in ("RX","TX"):
                continue
            extra_reservedpins=extra_reservedpins|{name:reservedpin}
        for pin in self.pins:
            is_pwm=False if pin in self.non_PWM_pins else True
            speciality=None
            if pin.pinname==self.sda:
                speciality="sda"
            elif pin.pinname==self.scl:
                speciality="scl"
            elif pin.pinname==self.onboard_led:
                speciality="OnBoardLed"
            elif pin.pinname==self.reservedpins["TX"]:
                speciality="TX"
            elif pin.pinname==self.reservedpins["RX"]:
                speciality="RX"
            elif pin.pinname in extra_reservedpins.keys():
                speciality=extra_reservedpins[pin.pinname]
            pindic=pin.to_dict(is_pwm,speciality)
            dic=dic|pindic
        self.pinmap=dic
    def export(self):
        self.to_dict()
        short_pins={}
        for pin,pin_dict in self.pinmap.items():
            short_pins=short_pins|{pin:pin_dict["actualpin"]}

        for pin, pin_dict in self.pinmap.items():
            if pin_dict["speciality"] is not None:short_pins = short_pins|{pin_dict["speciality"].upper():pin}

        short_pins={self.boardname:short_pins}
        origianaldata={}
        with open(path,"r") as file:
            origianaldata=BoardDataManager.load(file)
        with open(path,"w") as file:
            origianaldata=origianaldata|short_pins
            BoardDataManager.dump(origianaldata,file,indent=4)\
        
        
    def user_export(self, json_file:str, indent:int = 4):
        if not json_file.endswith(".json"):
            raise InvalidArgumentError(json_file, "string that ends with '.json'(the filename)")
        if not isinstance(indent,int):
            raise InvalidArgumentError(indent,"int")
        if not Path.exists(Path(json_file)):
            Path.touch(Path(json_file),exist_ok=True)
        with open(json_file,"r") as file:
            try:
                data=BoardDataManager.load(file)
            except BoardDataManager.JSONDecodeError:
                data={}
        with open(json_file,"w") as file:
            self.to_dict()
            if self.boardname==None:
                self.boardname=self.__class__.__name__
            data=data|{self.boardname:{
                "pins":self.pinmap,
                "Wifi":self.has_wifi,
                "BlueTooth":self.has_bluetooth,
                "EEPROM":self.has_EEPROM
                }
            }
            BoardDataManager.dump(data,file,indent=indent)
    def set_variables(self,pins,sda,scl,onboard_led,nonPWM_pins,TX,RX,reserved_pins,has_wifi=False,has_bluetooth=False,has_EEPROM=False):
        self.pins=pins
        self.sda=sda
        self.scl=scl
        self.onboard_led=onboard_led
        self.non_PWM_pins=nonPWM_pins
        self.TX=TX
        self.RX=RX
        self.reservedpins={"TX":TX,"RX":RX}|reserved_pins
        self.has_wifi=has_wifi
        self.has_bluetooth=has_bluetooth
        self.has_EEPROM=has_EEPROM
    def __str__(self):
        return self.boardname
class ArduinoUnoR3(Board):
    def setup(self):
        self.pins=MCUpin.generate_pin_array(6,14)
        self.sda="A4"
        self.scl="A5"
        self.onboard_led="13"
class ArduinoNano(Board):
    def setup(self):
        self.pins=MCUpin.generate_pin_array(8,14)
        self.sda="A4"
        self.scl="A5"
        self.onboard_led="14"
        self.non_PWM_pins=["A0","A1","A2","A3","A4","A5","A6","A7"]
        self.has_EEPROM=True

class HobbySparkBoard(Board):
    def setup(self):
        self.set_variables(MCUpin.generate_pin_array(12, 500), 34, 56, 11, ["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11"],1, 0, {"QWERTY pin":122}, has_EEPROM=True)
CURRENTBOARD:Board=None
