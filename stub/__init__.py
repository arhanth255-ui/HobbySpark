import inspect
import json
from .Boards import *
from .Devices.Classes import *
from .Devices.Constants import *
from .Devices.Functions import *
from .Devices.Classes.sharedInfo import set_board
from types import ModuleType,FunctionType
from pathlib import Path
import stub.Boards as currentboard_helper

VERSION="1.0.0"
NAME="HobbySpark Transpiler"
LOCAL=(
    "currentframe",
    "CURRENTBOARD",
    "pinvalue",
    "check",
    "board_check",
    "path",
    "Pin",
    "folder",
    "pins_in_dic",
    "modes_in_dic",
    "specialities_in_dic",
    "pins_and_modes",
    "pins_and_specialities",
    "PWM_pins",
    "pins",
    "INSPIRE",
    "DOUBT",
    "ERROR_NUMS",
    "LOCAL",
    "NAME",
    "VERSION",
    "get_all"
    
)
print("Hello, this is auto generated text from the HobbySpark transpiler.  ",
      
      "Before transpiling, you can run the file to get errors before transpiling, saving your time.",

      "All functions and methods print a string to the terminal to denote that a certain thing has happend. ",
    
      "-"*20+"Action strings"+"-"*20+"\n",

      sep="\n"
)

folder=Path(user_config_dir("HobbySpark transpiler", appauthor=False, roaming=True))
file=folder/"ClassData.json"

if not folder.exists():
      Path.mkdir(folder, parents=True, exist_ok=True)
if not file.exists():
      Path.touch(file, exist_ok=True)
op=False
dat=[]
with open(file, "r") as f:
      a = json.load(f)
      if not a:
            a = {"special":[]}
      dat=[]
      classes=[
            name for name, obj in globals().items()
            if inspect.isclass(obj)
      ]
      for name in classes:
            cl = globals()[name]
            if hasattr(cl, "meta"):
                  dat.append({"name":name}|cl.meta)
      else:
            dat.append({"name":name, "pin_args":{},"requires_updt":False,"requires_even":False})
      if a["special"]!=dat:
            op=True
if op:
      dat={"special":dat}
      with open(file,"w") as f:
            json.dump(dat, f, indent=4)



def get_current_board():
      return currentboard_helper.CURRENTBOARD

def getall():
      all=[name for name,obj in globals().items() 
         if not name in LOCAL
         and not name.startswith("_")
         and not isinstance(obj,ModuleType)
         ]
      print(sorted(all))

#getall()
__all__=['ActiveBuzzer', 'Analog', 'Any', 'ArduinoNano', 'ArduinoUnoR3', 'BLUE', 'BROWN', 'Board', 'BoardError', 'BoardNotDefinedError', 'BoardNotInitializedFirstError', 'Button', 'DARK_GRAY', 'DO_I_NEED_BRACES', 'DeviceNotCompatibleWithCurrentBoardError', 'Digital', 'Driver', 'EEPROM', 'FunctionType', 'GOLD', 'GRAY', 'GREEN', 'HobbySparkBoard', 'Http', 'I2C_LCD_Display', 'IMPORTANT', 'InvalidArgumentError', 'InvalidPinTypeError', 'LEFT', 'LIGHT_BLUE', 'LIGHT_GRAY', 'LIME', 'Led', 'MAGENTA', 'MCUpin', 'MS', 'MicroControllerError', 'ModuleType', 'NAVY', 'NOTE_A1', 'NOTE_A2', 'NOTE_A3', 'NOTE_A4', 'NOTE_A5', 'NOTE_A6', 'NOTE_A7', 'NOTE_AF1', 'NOTE_AF2', 'NOTE_AF3', 'NOTE_AF4', 'NOTE_AF5', 'NOTE_AF6', 'NOTE_AF7', 'NOTE_AS1', 'NOTE_AS2', 'NOTE_AS3', 'NOTE_AS4', 'NOTE_AS5', 'NOTE_AS6', 'NOTE_AS7', 'NOTE_B1', 'NOTE_B2', 'NOTE_B3', 'NOTE_B4', 'NOTE_B5', 'NOTE_B6', 'NOTE_B7', 'NOTE_BF1', 'NOTE_BF2', 'NOTE_BF3', 'NOTE_BF4', 'NOTE_BF5', 'NOTE_BF6', 'NOTE_BF7', 'NOTE_C1', 'NOTE_C2', 'NOTE_C3', 'NOTE_C4', 'NOTE_C5', 'NOTE_C6', 'NOTE_C7', 'NOTE_C8', 'NOTE_CS1', 'NOTE_CS2', 'NOTE_CS3', 'NOTE_CS4', 'NOTE_CS5', 'NOTE_CS6', 'NOTE_CS7', 'NOTE_D1', 'NOTE_D2', 'NOTE_D3', 'NOTE_D4', 'NOTE_D5', 'NOTE_D6', 'NOTE_D7', 'NOTE_DF1', 'NOTE_DF2', 'NOTE_DF3', 'NOTE_DF4', 'NOTE_DF5', 'NOTE_DF6', 'NOTE_DF7', 'NOTE_DS1', 'NOTE_DS2', 'NOTE_DS3', 'NOTE_DS4', 'NOTE_DS5', 'NOTE_DS6', 'NOTE_DS7', 'NOTE_E1', 'NOTE_E2', 'NOTE_E3', 'NOTE_E4', 'NOTE_E5', 'NOTE_E6', 'NOTE_E7', 'NOTE_EF1', 'NOTE_EF2', 'NOTE_EF3', 'NOTE_EF4', 'NOTE_EF5', 'NOTE_EF6', 'NOTE_EF7', 'NOTE_F1', 'NOTE_F2', 'NOTE_F3', 'NOTE_F4', 'NOTE_F5', 'NOTE_F6', 'NOTE_F7', 'NOTE_FS1', 'NOTE_FS2', 'NOTE_FS3', 'NOTE_FS4', 'NOTE_FS5', 'NOTE_FS6', 'NOTE_FS7', 'NOTE_G1', 'NOTE_G2', 'NOTE_G3', 'NOTE_G4', 'NOTE_G5', 'NOTE_G6', 'NOTE_G7', 'NOTE_GF1', 'NOTE_GF2', 'NOTE_GF3', 'NOTE_GF4', 'NOTE_GF5', 'NOTE_GF6', 'NOTE_GF7', 'NOTE_GS1', 'NOTE_GS2', 'NOTE_GS3', 'NOTE_GS4', 'NOTE_GS5', 'NOTE_GS6', 'NOTE_GS7', 'ORANGE', 'PINK', 'PURPLE', 'PassiveBuzzer', 'Path', 'PinAlreadyInUseError', 'PinError', 'PinNotApplicableError', 'PinOutOfRangeError', 'Potentiometer', 'RED', 'REST', 'RGB', 'RGBled', 'RIGHT', 'ReservedPinWarning', 'SEC', 'SKY_BLUE', 'SLIGHT_LEFT', 'SLIGHT_RIGHT', 'SerialMoniter', 'ServoMotor', 'TEAL', 'TwoWheeledDriver', 'UNIMPORTANT', 'US', 'UTMOST_IMPORTANCE', 'UltrasonicSensor', 'WHITE', 'Wifi', 'YELLOW', 'a', 'b', 'check_I2C_devices', 'cl', 'classes', 'dat', 'f', 'file', 'find_I2C_Devices', 'get_current_board', 'getall', 'interrupt', 'name', 'op', 'reserved_pin_warn', 'set_board', 'wait', 'warn']
#Comment off the __all__ after testing