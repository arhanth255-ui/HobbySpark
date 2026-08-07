from ..Boards import Board, MCUpin
class ArduinoUnoR3(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(6, 14)
        self.sda = "A4"
        self.scl = "A5"
        self.onboard_led = "13"
        self.nonPWM_pins = ["4", "7", "8", "12", "13", "A0", "A1", "A2", "A3", "A4", "A5"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoNano(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(8, 14)
        self.sda = "A4"
        self.scl = "A5"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoMega2560(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(16, 54)
        self.sda = "20"
        self.scl = "21"
        self.onboard_led = "13"
        self.nonPWM_pins = [
            "0","1","2","4","7","8","12","13","20","21",
            "A0","A1","A2","A3","A4","A5","A6","A7",
            "A8","A9","A10","A11","A12","A13","A14","A15"
        ]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoLeonardo(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(12, 14)
        self.sda = "2"
        self.scl = "3"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoMicro(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(12, 14)
        self.sda = "2"
        self.scl = "3"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoProMini(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(8, 14)
        self.sda = "A4"
        self.scl = "A5"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoMini(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(8, 14)
        self.sda = "A4"
        self.scl = "A5"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoNanoEvery(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(8, 14)
        self.sda = "A4"
        self.scl = "A5"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoUnoWiFiRev2(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(6, 14)
        self.sda = "A4"
        self.scl = "A5"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
        self.has_wifi = True
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True


class ArduinoLilyPad(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(6, 14)
        self.sda = "A4"
        self.scl = "A5"
        self.onboard_led = "13"
        self.nonPWM_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_EEPROM = True