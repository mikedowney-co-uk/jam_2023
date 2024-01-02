# Read from the Serial port ADC.
# Flash the LED if the signal saturates.

# Button 1 cycles through 1-2-4-8-16 averaging of the spectrum.
# Button 2 changes the scaling factor for the intensity.
# Potentiometer is read directly by the microcontroller to adjust the sample rate.

import serial
import scipy.fft as fft
import numpy as np
from time import sleep
import unicornhat as uh
import RPi.GPIO as GPIO

uh.set_layout(uh.HAT)
uh.rotation(0)
uh.brightness(0.5)

port = serial.Serial("/dev/serial0", baudrate=115200, parity=serial.PARITY_NONE, timeout=0.1)

fft_sizes = [256, 512, 1024, 2048, 4096]
fft_index = 0
points = fft_sizes[fft_index]

skip = 2  # skip the DC offset.

resampling = [1, 2, 4, 8]
res_index = 0

scalings = [4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25]
scale_index = 2

GPIO.setmode(GPIO.BOARD)
BUTTONS = [38, 40]
for p in BUTTONS:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
LED = 37
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)


def get_samples():
    saturated = GPIO.LOW
    samples = [0] * points
    for p in range(points):
        s = ord(port.read())
        samples[p] = s
        if s == 0 or s == 255:
            saturated = GPIO.HIGH
    GPIO.output(LED, saturated)
    port.reset_input_buffer()
    return samples


def get_fft(samples):
    transform = fft.fft(samples)
    spectrum = np.abs(transform[skip:skip + points // 2])
    # Downsample the array
    return np.mean(spectrum.reshape(-1, resampling[res_index]), 1)


c1 = 5000
c2 = 10000
c3 = 15000


def spect2hsv(v):
    if v <= 50:
        return 0, 0, 0
    if v < c1:
        return 0, 1, (v / c1) * (v / c1)
    if v < c2:
        return (v - c1) / ((c2 - c1) / 0.6), 1, 0.5
    return 0.6, min(1.0, (c3 - v) / c2), min(1.0, 0.5 + (v - c2) / c3)


def show_spectrum(spectrum):
    c = 0
    scale = scalings[scale_index]
    for y in range(8):
        for x in range(8):
            p = spectrum[c] * scale
            c += 1
            h, s, v = spect2hsv(p)
            uh.set_pixel_hsv(x, y, h, s, v)
    uh.show()


def parse_buttons():
    global res_index, scale_index, points, fft_index, points
    if GPIO.input(BUTTONS[0]) == 0:
        #		res_index += 1
        #		if res_index>=len(resampling):
        #			res_index=0
        #		print("Downsampling =",resampling[res_index])
        fft_index += 1
        if fft_index >= len(fft_sizes):
            fft_index = 0
        points = fft_sizes[fft_index]
        print("FFT size =", points)
        return True
    if GPIO.input(BUTTONS[1]) == 0:
        scale_index += 1
        if scale_index >= len(scalings):
            scale_index = 0
        print("Scale =", scalings[scale_index])
        return True
    return False


def destroy():
    print("Shutting Down...")
    GPIO.output(LED, GPIO.HIGH)  # led off
    GPIO.cleanup()  # Release resource
    port.close()


def loop():
    global points
    print("Running")
    while True:
        samples = get_samples()
        spectrum = get_fft(samples)
        show_spectrum(spectrum)
        pressed = parse_buttons()
        if pressed:
            print("Min =", min(samples), " Max =", max(samples), " FFTmin =", min(spectrum), " FFTmax=", max(spectrum))
            sleep(0.1)
        sleep(0.01)


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
