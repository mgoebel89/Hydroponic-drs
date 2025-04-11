from machine import Pin, Timer
from time import sleep_ms

PIN_PUMP = 23
PIN_LED_GREEN = 21
PIN_LED_RED = 20
PIN_BUTTON_GREEN = 19
PIN_BUTTON_RED = 18

# Set timings
counter_period = 1000 # in ms
time_off = 5 # in increments of counter period
time_on = 10 # in increments of counter period

timer_count = 0 # used for time keeping
sequence = 0 # used to keep up execution order
state = False # used to track automation state

# Set to True to get debug Prints
debug = False
debug_interval = 100

# Initialize output pins
pump = Pin(PIN_PUMP, Pin.OUT)
led_g = Pin(PIN_LED_GREEN, Pin.OUT)
led_r = Pin(PIN_LED_RED, Pin.OUT)

# Sets output pins to known state
pump.off()
led_g.off()
led_r.off()

# Initialize input pins
btn_g = Pin(PIN_BUTTON_GREEN, Pin.IN, Pin.PULL_DOWN)
btn_r = Pin(PIN_BUTTON_RED, Pin.IN, Pin.PULL_DOWN)

def print_debug(t):
    global pump, led_g, led_r, btn_g, btn_r, timer_count, sequence, state
    debug_info = {
        "Pump": pump.value(),
        "LED_G": led_g.value(),
        "LED_R": led_r.value(),
        "BTN_G": btn_g.value(),
        "BTN_R": btn_r.value(),
        "Period count": timer_count,
        "Sequence": sequence,
        "State": state
    }
    print("==================")
    for key, value in debug_info.items():
        print(f"{key}: {value}")

if debug:
    debug_timer = Timer(2)
    debug_timer.init(period=debug_interval, mode=Timer.PERIODIC, callback=print_debug)

def tf(t):
    # Increments timer variable
    global timer_count
    timer_count += 1

# Sets up timer
tim = Timer(0)

def callback_button_green(pin):
    # Called when green button is pressed
    global state, pump, tim, debug, sequence, timer_count
    if debug:
        print(f"Green, State: {state}")
    if state:
        pass
    else:
        pump.on()
        sequence = 1
        timer_count = 0
        state = True
    tim.init(period=counter_period, mode=Timer.PERIODIC, callback=tf) # Enable timer

def callback_button_red(pin):
    # Called when red button is pressed
    global state, pump, tim, debug, sequence, timer_count
    if debug:
        print(f"Red, State: {state}")
    tim.deinit() # Disable timer
    if state:
        pump.off()
        sequence = 0
        timer_count = 0
        state = False
    else:
        pass

# Setup callback functions for button-press interrupts
btn_g.irq(trigger=Pin.IRQ_RISING, handler=callback_button_green)
btn_r.irq(trigger=Pin.IRQ_RISING, handler=callback_button_red)

while True:
    # Update LEDs to reflect execution status
    led_g.value(state)
    led_r.value(not state)

    if state and sequence == 0 and timer_count >= time_off:
        pump.on()
        sequence = 1
        timer_count = 0
    if state and sequence == 1 and timer_count >= time_on:
        pump.off()
        sequence = 0
        timer_count = 0
