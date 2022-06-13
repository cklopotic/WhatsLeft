# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageChops
from adafruit_rgb_display import ili9341


# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the display:
disp = ili9341.ILI9341(
    spi,
    rotation=0,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

# Load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)

image =  Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

#Constants
ROW_HEIGHT = 20
SCREEN_WHOLE = (0, 0, width, height)
WEIGHT_TEXT = (0, 0, width, ROW_HEIGHT)
UNITS_TEXT = (0, ROW_HEIGHT, width, ROW_HEIGHT*2)
GAUGEx = width-ROW_HEIGHT*2
GAUGEy = ROW_HEIGHT*2
GAUGE = (GAUGEx, GAUGEy, width, height)
LOGOx1 = 0
LOGOy1 = ROW_HEIGHT*2
LOGO_WIDTH = width-ROW_HEIGHT*2
LOGO_HEIGHT = height - ROW_HEIGHT*2

def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

def draw_percent_2_GaugeY1(draw, percent):
    pixel_total = height - GAUGEy
    percent = clamp(percent, 0, 100)
    gaugeY1 = height - ((pixel_total * percent) // 100)
    red = 255 - round(percent * 2.55)
    green = round(percent * 2.55)
    
    # Draw placeholder/Background for Gauge
    draw.rectangle(GAUGE, outline=0, fill=(25,25,25))
    #draw filled portion
    draw.rectangle((GAUGEx, gaugeY1, width, height), outline=0, fill=(red,green,0))
    
    #draw text
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    if (percent > 98):
        pec_txtY1 = gaugeY1
    else:
        pec_txtY1 = gaugeY1 - font2.getsize(f'{percent}%')[1]
    draw.text((GAUGEx +2, pec_txtY1), f'{percent}%', font=font2, fill="#FFFFFF")
    return

def setup():
    draw = ImageDraw.Draw(image)
    # Draw a black filled box to clear the image.
    draw.rectangle(SCREEN_WHOLE, outline=0, fill=(0, 0, 0))
        
    logo = Image.open("/home/busch/Documents/WhatsLeft/buschLight.jpeg")

    # Scale the image to the smaller screen dimension
    image_ratio = logo.width / logo.height
    screen_ratio = LOGO_WIDTH / LOGO_HEIGHT
    if screen_ratio < image_ratio:
        scaled_width = logo.width * LOGO_HEIGHT // logo.height
        scaled_height = LOGO_HEIGHT
    else:
        scaled_width = LOGO_WIDTH
        scaled_height = logo.height * LOGO_WIDTH // logo.width
    logo = logo.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - LOGO_WIDTH // 2
    y = scaled_height // 2 - LOGO_HEIGHT // 2
    logo = logo.crop((x, y, x + LOGO_WIDTH, y + LOGO_HEIGHT))
    image.paste(logo, (0,ROW_HEIGHT*2))
    
    draw = ImageDraw.Draw(image)
    # Draw placeholder/Background for Gauge
    draw.rectangle(GAUGE, outline=0, fill=(25,25,25))

    
    # Display image.
    disp.image(image)
    return (image)
    
def update(background, weight, percent, units):
    weight_lbs = f'Approx Beer Remaining: {weight} lbs'
    units_left = f'Approx Drinks Remaining: {units}'
    
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(background)
    
    #clear Text window
    draw.rectangle((0,0,width,ROW_HEIGHT*2), outline=0, fill=(0,0,0))
    
    # First define some constants to allow easy positioning of text.
    padding = 2
    x = 0

    # Write text.
    y = padding
    draw.text((x, y), weight_lbs, font=font, fill="#0000FF")
    y += font.getsize(weight_lbs)[1]
    draw.text((x, y), units_left, font=font, fill="#0000FF")
        
    # Draw Percent level shape for Gauge
    draw_percent_2_GaugeY1(draw, percent)

    # Display image.
    disp.image(background)
