import machine
import micropython
import time

led = machine.Pin(25, machine.Pin.OUT)
sense = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
micropython.alloc_emergency_exception_buf(100)
interrupt_flag = False

# -- OK
# while True:
#     while sense.value() == 1:
#         pass
#     led.off()
#     while sense.value() == 0:
#         pass
#     led.on()

# -- OK
# last_x = 0
# while True:
#     x = sense.value()
#     if last_x != x:
#         print ("value is: " + str(x), end="\r")
#         last_x = x
#     led.value(x)

# -- OK
# while True:
#     while sense.value() == 1:
#         pass
#     print ("value is: 0", end="\r")
#     led.off()
#     while sense.value() == 0:
#         pass
#     print ("value is: 1", end="\r")
#     led.on()

def isr(x):
    global interrupt_flag
    interrupt_flag = True
    

sense.irq(handler = isr, trigger = machine.Pin.IRQ_FALLING, hard = True)

start_flag = True
start_us = time.ticks_us()
while True:
    if interrupt_flag:
        # machine.disable_irq()
        interrupt_flag = False
        led.toggle()
        # machine.enable_irq()
        if start_flag:
            start_flag = False
            start_us = time.ticks_us()
        else:
            end_us = time.ticks_us()
            period_us = end_us - start_us
            start_us = end_us
            print("frequency: " + str(1000000/period_us), end="\r")

