import sys
import time
from time import perf_counter
import logging
from typing import Union

import pygame
from RPi import GPIO
from pygame import Rect, Surface, SurfaceType
from pygame.font import Font

INPUT_PIN = 21

logging.basicConfig(filename='geiger.log',
                    filemode='a',
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('geiger')

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)

surface: Surface  # uninitialised
font: Font  # uninitialised

WIDTH = 480
HEIGHT = 320

# Plotting and max value
counts = [0] * WIDTH
counts[0] = 25
plot_loc = 0

#  instantaneous value (cpm based on the last 5 clicks) and medium term average (last 10 readings)
COUNTS = 5
NUM_VALUES = 10
values = [0] * NUM_VALUES
value_pos = 0
current = 0
mx = 0
avg = 0

# to black out where the text gets drawn
r = Rect(0, 0, WIDTH, 20)


def show_text(text, pos, fg=(255, 255, 255), bg=(0, 0, 0)):
    x, y = pos
    textobj = font.render(text, True, fg, bg)
    textobj.set_alpha(128)
    surface.blit(textobj, (x, y))


def mean_ignore_zeros(vals):
    has_values = [c for c in vals if c != 0]
    return sum(has_values) / len(has_values)


def setup():
    global surface, font
    pygame.init()
    surface = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
    font = pygame.font.Font('freesansbold.ttf', 20)
    pygame.event.pump()
    logger.info("Starting")
    show_values()
    pygame.display.update()


def wait_single_click():
    """Wait for a high->low"""
    while GPIO.input(INPUT_PIN) == 1:
        pass
    while GPIO.input(INPUT_PIN) == 0:
        pass


def wait_clicks():
    """returns instantaneous CPM value based on time for 5 clicks"""
    start = perf_counter()
    for i in range(COUNTS):
        wait_single_click()
    took = perf_counter() - start
    logger.info("%d clicks in %0.2f s" % (COUNTS, took))
    return 60.0 / (took / COUNTS)


def get_reading():
    global value_pos, current
    current = wait_clicks()
    values[value_pos] = current
    value_pos = (value_pos + 1) % NUM_VALUES
    add_value(current)


def show_values():
    global mx, avg
    mx = max(counts)
    avg = mean_ignore_zeros(counts)
    pygame.draw.rect(surface, (0, 0, 0), r)
    show_text("counts: %d" % current, [0, 0], fg=(0, 255, 0))
    show_text("mean: %0.2f" % avg, [150, 0])
    show_text("max: %d" % mx, [320, 0], fg=(255, 0, 0))


def add_value(v):
    global plot_loc
    counts[plot_loc] = v
    plot_loc = (plot_loc + 1) % WIDTH


def plot_readings():
    global current
    v = int(min(current, 255))
    logger.info("current:%0.2f max:%0.2f mean:%0.2f" % (current, mx, avg))
    # Draw the count bars
    pygame.draw.line(surface, (0, 255, 0), (plot_loc, HEIGHT), (plot_loc, HEIGHT - v))
    pygame.draw.line(surface, (0, 0, 128), (plot_loc, HEIGHT - v), (plot_loc, HEIGHT - 255))

    # Plot the mean and max values
    surface.set_at((plot_loc, HEIGHT - int(mx)), (255, 0, 0))
    surface.set_at((plot_loc, HEIGHT - int(avg)), (255, 255, 255))


if __name__ == "__main__":
    setup()
    for i in range(50000):
        try:
            get_reading()
            plot_readings()
            show_values()
            pygame.display.update()
            pygame.event.clear()
        except:
            logger.exception("main loop")
            raise
        # time.sleep(0.1)
    logger.info("Done")
    time.sleep(5)
    logger.info("Exit")
    pygame.quit()
    sys.exit()
