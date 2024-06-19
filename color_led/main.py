from machine import Pin, PWM
import time
import random
import math

RED_PIN   = 20   # red led pin
GREEN_PIN = 21   # green led pin
BLUE_PIN  = 22   # blue led pin

RED      = 0
GREEN    = 1
BLUE     = 2
N_COLORS = 3

MIN_PERIOD = 5       # seconds
MAX_PERIOD = 10       # seconds
FREQUENCY  = 1000     # pwm frequency in hertz
SLEEP_TIME = 0.001    
MAX_DUTY   = 255 * 255 / 2

class Color:
    def __init__(self, pin : int, name : str, max_duty : int, frequency : int) -> None:
        self.pin = pin
        self.name = name
        self.enabled = False
        self.duty = 0
        self.max_duty = max_duty
        self.frequency = frequency
        self.period = 0
        self.time = 0
        self.pwm = PWM(Pin(self.pin))
        self.pwm.freq(self.frequency)
        self.pwm.duty_u16(self.duty)
        
    def set_duty(self, duty : int) -> None:
        self.duty = duty
        self.pwm.duty_u16(self.duty)
        
    def generate_period(self) -> None:
        self.period = int(MIN_PERIOD + (MAX_PERIOD - MIN_PERIOD) * random.random())

    def next_duty(self) -> None:
        if self.enabled:
            self.time += SLEEP_TIME
            sin_arg = 2 * math.pi * self.time / self.period - math.pi / 2
            duty = int(self.max_duty * (1 + math.sin(sin_arg)) / 2)
            self.set_duty(duty)
            
    def set_enabled(self, enabled : bool) -> None:
        self.enabled = enabled
        if self.enabled:
            self.generate_period()
            self.time = 0
            # print(self.name + " " + str(self.period))
        else:
            self.set_duty(0)
            self.period = 0
            self.time = 0
            
    def is_period_exceeded(self) -> bool:
        if self.enabled:
            return self.time > self.period
        else:
            return False

class LED:
    def __init__(self, max_duty : int, frequency : int) -> None:
        self.red   = Color(RED_PIN,   "red",   max_duty, frequency)
        self.green = Color(GREEN_PIN, "green", max_duty / 2, frequency)
        self.blue  = Color(BLUE_PIN,  "blue",  max_duty, frequency)
        self.colors = [self.red, self.green, self.blue]
        self.colors[RED].set_enabled(True)
        self.colors[GREEN].set_enabled(True)
        self.colors[BLUE].set_enabled(False)
        self.disabled_color = BLUE
        
    def set_frequency(self, frequency : int) -> None:
        for c in self.colors:
            c.frequency = frequency
            
    def set_duty(self, duty : int) -> None:
        for c in self.colors:
            c.set_duty(duty)
            
    def tick(self) -> None:
        for c in self.colors:
            c.next_duty()
            
    def is_period_exceeded(self):
        for i, c in enumerate(self.colors):
            if c.is_period_exceeded():
                return True, i
        return False, -1
    
    def switch_disabled(self, color_index : int) -> None:
        self.colors[color_index].set_enabled(False)
        self.colors[self.disabled_color].set_enabled(True)
        self.disabled_color = color_index    

#while (True):
#    pass

# Main program
led = LED(MAX_DUTY, FREQUENCY)

while (True):        
    has_exceeded, color_index = led.is_period_exceeded()
    if has_exceeded:
        led.switch_disabled(color_index)
        
    led.tick()
    time.sleep(SLEEP_TIME)