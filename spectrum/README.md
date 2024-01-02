# Pi based Spectrum Analyzer

Uses `scipy` to perform an FFT on a sampled waveform and displays the result on an 8x8 LED matrix.

## Description of the system

![Lego. Pi. Unicorns.](pi2_spectrum_analyzer.jpg)

From top to bottom:
1. Microcontroller - reads an analogue signal and sends it to the Pi through the serial port
2. Raspberry Pi with the Pimoroni Unicorn Hat on top
3. Board with a potentiometer, 2 buttons and an LED:
   * Potentiometer is read by the microcontroller to adjust the sample rate
   * First button adjusts the FFT width
   * Second button changes the scale used to calculate the LED intensity and colour
   * LED lights up if the signal saturates
4. Amplifier with gain and offset so the signal can be shifted to fit within the 0-3.3v range expected
5. Microphone
6. Voltage regulator for the amplifier, providing a -5v supply.

## The Code

Unfortunately I don't have the microcontroller code available but what it does is:
* Reads the ADC and sends the value to the serial port
* Reads the potentiometer and pauses according to the value (so changing the potentiometer adjusts the sample rate)

The python code reads in a block of values, performs an FFT and uses the results to
set the colours and intensities of the LED matrix. 