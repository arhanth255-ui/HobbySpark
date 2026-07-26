from stub import *

def blink(led:int)->Led:
    led_n=Led(led)
    return led_n

def blinker(led:int)->Led:
    return led

def helloworld(led:int,ghe:int)->float:
    return led,ghe

class hello(Led):
    pass
led=blink(1)
while 1>2:
    led=blink(1)


