# Butterfly LEDs

![LED Butterfly](/Users/mike.downey/Documents/Python/jam_2023/butterfly/butterfly.jpg)

## Wiring Up

The setup I used had several sets of LEDs each wired in parallel:
 * 4 RGB LEDs
 * 10mm Blue LEDs
 * 5mm separate red, green blue
 * 3mm white LEDs

This required 8 GPIO pins in total so as well as working on an original Pico, it also works
on smaller ones (such as the Tiny 2040) which have fewer pins.

## To Use:

1. Edit `common.py` to hold the correct GPIO pins.
2. Rename either `pulse.py` or `flash.py` to `main.py` and copy to the pico.
3. Copy `led_common.py`  to the pico.
