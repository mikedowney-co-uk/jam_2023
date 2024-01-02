from machine import Pin, PWM
import machine

# Pins for Pico
# gpios = [8, 9, 10, 11, 12, 13, 14, 15]

# Pins for Tiny2040
gpios = [0, 1, 2, 3, 4, 5, 6, 7]
builtins = [18, 19, 20]

# Last 3 are the built-in LED

def setup_pins():
    pad_control_registers = 0x4001c004
    for g in gpios:
        address = pad_control_registers + 4 * g
        machine.mem32[address] = machine.mem32[address] | 0b0110000
    leds = [Pin(g, Pin.OUT) for g in gpios]
    for l in leds:
        l.low()
    # Turn built-in LEDs off
    for b in builtins:
        Pin(b, Pin.OUT).high()
    return leds


def setup_pwm():
    leds = [PWM(Pin(g), duty_u16=0, freq=50000) for g in gpios]
    return leds
