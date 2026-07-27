from ..Boards import Board, MCUpin
class ESP32DevKit(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(20, 40)
        self.sda = "21"
        self.scl = "22"
        self.onboard_led = "2"
        self.RX = "3"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "3"}
        self.has_wifi = True
        self.has_bluetooth = True


class ESP32S2(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(20, 43)
        self.sda = "8"
        self.scl = "9"
        self.onboard_led = "15"
        self.RX = "44"
        self.TX = "43"
        self.reserved_pins = {"TX": "43", "RX": "44"}
        self.has_wifi = True


class ESP32S3(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(20, 48)
        self.sda = "8"
        self.scl = "9"
        self.onboard_led = "13"
        self.RX = "44"
        self.TX = "43"
        self.reserved_pins = {"TX": "43", "RX": "44"}
        self.has_wifi = True
        self.has_bluetooth = True


class ESP32C3(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(6, 21)
        self.sda = "8"
        self.scl = "9"
        self.onboard_led = "8"
        self.RX = "20"
        self.TX = "21"
        self.reserved_pins = {"TX": "21", "RX": "20"}
        self.has_wifi = True
        self.has_bluetooth = True


class ESP8266NodeMCU(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(1, 10)
        self.sda = "D2"
        self.scl = "D1"
        self.onboard_led = "D4"
        self.RX = "RX"
        self.TX = "TX"
        self.reserved_pins = {"TX": "TX", "RX": "RX"}
        self.has_wifi = True


class ESP8266D1Mini(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(1, 8)
        self.sda = "D2"
        self.scl = "D1"
        self.onboard_led = "D4"
        self.RX = "RX"
        self.TX = "TX"
        self.reserved_pins = {"TX": "TX", "RX": "RX"}
        self.has_wifi = True


class RaspberryPiPico(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 28)
        self.sda = "GP4"
        self.scl = "GP5"
        self.onboard_led = "LED"
        self.RX = "GP1"
        self.TX = "GP0"
        self.reserved_pins = {"TX": "GP0", "RX": "GP1"}


class RaspberryPiPicoW(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 28)
        self.sda = "GP4"
        self.scl = "GP5"
        self.onboard_led = "LED"
        self.RX = "GP1"
        self.TX = "GP0"
        self.reserved_pins = {"TX": "GP0", "RX": "GP1"}
        self.has_wifi = True


class ArduinoNanoESP32(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 21)
        self.sda = "11"
        self.scl = "12"
        self.onboard_led = "13"
        self.RX = "44"
        self.TX = "43"
        self.reserved_pins = {"TX": "43", "RX": "44"}
        self.has_wifi = True
        self.has_bluetooth = True


class ArduinoGigaR1(Board):
    def setup(self):
        self.pins = MCUpin.generate_pin_array(0, 76)
        self.sda = "20"
        self.scl = "21"
        self.onboard_led = "LED_BUILTIN"
        self.RX = "0"
        self.TX = "1"
        self.reserved_pins = {"TX": "1", "RX": "0"}
        self.has_wifi = True
        self.has_bluetooth = True