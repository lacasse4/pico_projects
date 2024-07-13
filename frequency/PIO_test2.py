from machine import Pin
import utime
from SMCounter import SMCounter

counter = SMCounter(smID=0,InputPin=Pin(14,Pin.IN,Pin.PULL_UP))

while True:
    print(counter.value())
    counter.reset()
    utime.sleep(1)