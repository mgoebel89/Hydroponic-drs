from machine import ADC, Pin
import time

# Setup ADC (GPIO36 on ESP32)
ph_pin = ADC(Pin(36))       # Change to your actual pin
ph_pin.atten(ADC.ATTN_11DB)  # For 0-3.6V input range
ph_pin.width(ADC.WIDTH_12BIT)

def read_ph():
    raw = ph_pin.read()
    voltage = raw / 4095 * 3.3  # 12-bit ADC to voltage
    ph = 7 + ((2.5 - voltage) * 3.5)  # Rough linear mapping
    return ph, voltage

while True:
    ph, voltage = read_ph()
    print("pH:", round(ph, 2), "Voltage:", round(voltage, 2), "V")
    time.sleep(1)
