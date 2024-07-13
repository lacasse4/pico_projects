import micropython
from machine import Pin, mem32
from time import sleep

led = Pin(25, machine.Pin.OUT)
sense = Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
micropython.alloc_emergency_exception_buf(100)

first = True
done = True
TIMERLR1 = 0
TIMERLR2 = 0
TIMER_BASE = 0x40054000
TIMERLR_ADDR = TIMER_BASE + 0x0c
TIMERHR_ADDR = TIMER_BASE + 0x08
TIMERAWL_ADDR = TIMER_BASE + 0x28

@micropython.native
def isr(x):
    global first, done, TIMERLR1, TIMERLR2
    if not first:
        TIMERLR1 = mem32[TIMERAWL_ADDR]
        #mem32[TIMERHR_ADDR]  # flush TIMERHR
        first = True
        return
    
    if not done:
        TIMERLR2 = mem32[TIMERAWL_ADDR]
        #mem32[TIMERHR_ADDR]  # flush TIMERHR
        done = True
        return
    
sense.irq(handler = isr, trigger = machine.Pin.IRQ_FALLING, hard = True)

last_frequency = 0
while True:
    state = machine.disable_irq()
    first = False
    done = False
    machine.enable_irq(state)

    while not done:
        pass
    
    frequency = 1_000_000/(TIMERLR2-TIMERLR1);
    print(frequency, abs(last_frequency-frequency), end="        \r")
    last_frequency = frequency
    sleep(0.1)
