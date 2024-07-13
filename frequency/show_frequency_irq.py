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

MAX_BUFF = 5
period_us_list = []
print_time = time.ticks_ms()
start_flag = True
while True:
    if interrupt_flag:
        # machine.disable_irq()
        interrupt_flag = False
        # led.toggle()
        # machine.enable_irq()
        if start_flag:
            start_flag = False
            start_us = time.ticks_us()
        else:
            end_us = time.ticks_us()
            period_us = time.ticks_diff(end_us, start_us)
            start_us = end_us

    if time.ticks_ms() - print_time > 200:
        print_time = time.ticks_ms()
        period_us_list.append(period_us)
        
        if len(period_us_list) == MAX_BUFF:
            period_us_max = max(period_us_list)
            period_us_min = min(period_us_list)
            period_us_list.clear()
            middle_us = (period_us_max + period_us_min) / 2
            gap_us = period_us_max - period_us_min
            error_pct_us = 100 * gap_us / middle_us
            frequency_us = 1000000 / middle_us
            
            print("freq_us: %6.1f" % (frequency_us), end=" ")
            print("prec_us: %4.2f" % (error_pct_us), end="    \r")
        