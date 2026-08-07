from stub import *
set_board(ArduinoNano(), debug_mode=True)
lcd = I2C_LCD_Display("SDA","SCL",16,2,0x28)
lcd.scroll_with_millis("", 1, SEC)
lcd.add("Hello world from HobbySpark")