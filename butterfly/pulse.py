import time
from led_common import setup_pins, setup_pwm
from random import randint

MAX_VALUE = 25000

# PWM fade the LEDs on and off

pwm_speeds = []
pwm_values = []
wait_until_change = []


def set_pwm_speed(i):
    global pwm_speeds
    pwm_speeds[i] = randint(5, 20)
    print(i, pwm_speeds[i])


def init_pwm_values(n):
    global pwm_speeds, pwm_values, wait_until_change
    pwm_values = [0] * n
    pwm_speeds = [0] * n
    wait_until_change = [0] * n
    for i in range(n):
        set_pwm_speed(i)


def update_pwm_values(n):
    global pwm_values
    for i in range(n):
        pwm_values[i] = pwm_values[i] + pwm_speeds[i]
        if pwm_values[i] < -MAX_VALUE:
            pwm_values[i] = -MAX_VALUE
            pwm_speeds[i] = -pwm_speeds[i]
            print("Reversing", i)
            if randint(0, 100) == 1:
                set_pwm_speed(i)
        if pwm_values[i] > MAX_VALUE:
            pwm_values[i] = MAX_VALUE
            pwm_speeds[i] = -pwm_speeds[i]


def run(all_leds):
    while (True):
        for i, l in enumerate(all_leds):
            l.duty_u16(pwm_values[i] if pwm_values[i] > 0 else 0)
        update_pwm_values(len(all_leds))
        time.sleep_ms(1)


if __name__ == "__main__":
    setup_pins()
    all_leds = setup_pwm()
    init_pwm_values(len(all_leds))
    run(all_leds)
