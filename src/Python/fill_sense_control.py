from machine import Pin, Timer
from time import sleep_ms

PIN_PUMP = 23
PIN_LED_GREEN = 21
PIN_LED_RED = 20
PIN_BUTTON_GREEN = 19
PIN_BUTTON_RED = 18
PIN_FILL_HIGH = 9
PIN_FILL_LOW = 15

# Set timings
counter_period = 1000 # in ms
time_off = 5 # in increments of counter period
time_rest = 10 # in increments of counter period
time_drain = 15 # in increments of counter period

timer_count = 0 # used for time keeping
sequence = 0 # used to keep up execution order
state = False # used to track automation state
filling = False # used to keep track of automation state
draining = False # used to keep track of automation state

# Set to True to get debug Prints
debug = False
# Set debug interval in ms
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
fill_high = Pin(PIN_FILL_HIGH, Pin.IN, Pin.PULL_UP)
fill_low = Pin(PIN_FILL_LOW, Pin.IN, Pin.PULL_UP)

def print_debug(t):
    global pump, led_g, led_r, btn_g, btn_r, fill_high, fill_low, timer_count, sequence, state, filling
    print(f"==================")
    print(f"Pump: {pump.value()}")
    print(f"LED_G: {led_g.value()}")
    print(f"LED_R: {led_r.value()}")
    print(f"BTN_G: {btn_g.value()}")
    print(f"BTN_R: {btn_r.value()}")
    print(f"FILL_HIGH: {fill_high.value()}")
    print(f"FILL_LOW: {fill_low.value()}")
    print(f"Period count: {timer_count}")
    print(f"Sequence: {sequence}")
    print(f"State: {state}")
    print(f"Filling: {filling}")
    print(f"Draining: {draining}")

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
    global state, pump, tim, debug, sequence, timer_count, filling, draining
    if debug:
        print(f"Green, State: {state}")
    if state:
        pass
    else:
        pump.on()
        filling = True
        draining = False
        sequence = 1
        timer_count = 0
        state = True
    tim.init(period=counter_period, mode=Timer.PERIODIC, callback=tf) # Enable timer

def callback_button_red(pin):
    # Called when red button is pressed
    global state, pump, tim, debug, sequence, timer_count, filling
    if debug:
        print(f"Red, State: {state}")
    tim.deinit() # Disable timer
    if state:
        sequence = 0
        timer_count = 0
        state = False
        if filling:
            pump.on()
    else:
        pass

# Setup callback functions for button-press interrupts
btn_g.irq(trigger=Pin.IRQ_RISING, handler=callback_button_green)
btn_r.irq(trigger=Pin.IRQ_RISING, handler=callback_button_red)

while True:
    # Update LEDs to reflect execution status
    led_g.value(state)
    led_r.value(not state)
    
    # Check if automation isn't running, disable pump after full
    if not state and filling:
        if fill_high.value() == 0:
            pump.off()
            filling = False
            sequence = 0
            timer_count = 0

    # Run sequence step 0 if automation is running and timer has exceeded threshold
    if state and sequence == 0 and timer_count >= time_off:
        pump.on()
        filling = True
        draining = False
        sequence = 1
        timer_count = 0

    # Run sequence step 1 if automation is running and water has reached the lower threshold
    if state and sequence == 1 and fill_low.value() == 0:
        pump.off()
        filling = True
        draining = False
        sequence = 2
        timer_count = 0
    
    # Run sequence step 2 if automation is running and timer has exceeded threshold
    if state and sequence == 2 and timer_count >= time_rest:
        pump.on()
        filling = True
        draining = False
        sequence = 3
        timer_count = 0

    # Run sequence step 3 if automation is running and water has reached the upper threshold
    if state and sequence == 3 and fill_high.value() == 0:
        pump.off()
        filling = False
        draining = True
        sequence = 4
        timer_count = 0

    # Run sequence step 4 if automation is running and timer has exceeded threshold
    if state and sequence == 4 and timer_count >= time_drain:
        draining = False
        sequence = 0
        timer_count = 0