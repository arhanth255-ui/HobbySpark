from ..Boards import Board, MCUpin
class ArduinoDue(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(12, 53)
        self.sda = "20"
        self.scl = "21"
        self.onboard_led = "13"
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}


class ArduinoZero(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 21)
        self.sda = "20"
        self.scl = "21"
        self.onboard_led = "13"
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}


class STM32BluePill(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 37)
        self.sda = "PB7"
        self.scl = "PB6"
        self.onboard_led = "PC13"
        self.RX = "PA10"
        self.TX = "PA9"
        self.reserved_pins = {"TX": "PA9", "RX": "PA10"}


class STM32BlackPill(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 47)
        self.sda = "PB7"
        self.scl = "PB6"
        self.onboard_led = "PC13"
        self.RX = "PA10"
        self.TX = "PA9"
        self.reserved_pins = {"TX": "PA9", "RX": "PA10"}


class Teensy40(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 33)
        self.sda = "18"
        self.scl = "19"
        self.onboard_led = "13"
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}


class Teensy41(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 41)
        self.sda = "18"
        self.scl = "19"
        self.onboard_led = "13"
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}


class AdafruitFeatherM0(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 20)
        self.sda = "20"
        self.scl = "21"
        self.onboard_led = "13"
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}


class AdafruitFeatherESP32S2(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 44)
        self.sda = "8"
        self.scl = "9"
        self.onboard_led = "13"
        self.RX = "44"
        self.TX = "43"
        self.reserved_pins = {"TX": "43", "RX": "44"}
        self.has_wifi = True


class SeeeduinoXIAO(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 10)
        self.sda = "4"
        self.scl = "5"
        self.onboard_led = "13"
        self.RX = "7"
        self.TX = "6"
        self.reserved_pins = {"TX": "6", "RX": "7"}


class SeeeduinoXIAOESP32C3(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 21)
        self.sda = "6"
        self.scl = "7"
        self.onboard_led = "8"
        self.RX = "21"
        self.TX = "20"
        self.reserved_pins = {"TX": "20", "RX": "21"}
        self.has_wifi = True
        self.has_bluetooth = True