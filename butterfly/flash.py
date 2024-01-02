import time
from random import randint
from led_common import setup_pins


# Flash the LEDs on and off

def leds_on(leds, number):
    for i in range(len(leds)):
        if i < number:
            leds[i].high()
            print(leds[i], "on")
        else:
            leds[i].low()
            print(leds[i], "off")


def shuffle(oldlist):
    newlist = []
    l = len(oldlist)
    while len(newlist) < l:
        pos = randint(0, l - 1)
        value = oldlist[pos]
        if value not in newlist:
            newlist.append(value)
    return newlist


def run(leds):
    while (True):
        leds = shuffle(leds)
        print(leds)
        leds_on(leds, randint(1, 4))
        time.sleep_ms(500)


if __name__ == "__main__":
    all_leds = setup_pins()
    run(all_leds)
