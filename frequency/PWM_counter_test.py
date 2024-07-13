from machine import Pin
from PWMCounter import PWMCounter
from time import sleep

output = Pin(2, Pin.OUT)
output.value(1)

# Initiate counter on pin 15
counter = PWMCounter(15, "EDGE_FALLING")
# Start counter
counter.start()

while True:
    # Generate single pulse
    output.value(0)
    output.value(1)
    # Print counter value
    print(counter.read())
    sleep(1)