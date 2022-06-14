import RPi.GPIO as GPIO                # import GPIO
from hx711 import HX711                # import the class HX711
  
GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
hx = HX711(dout_pin=21, pd_sck_pin=20)

#scale calibration constants
OFFSET = 161969
KNOWN_WEIGHT_LBS = 120 #item used at this known weight to calibrate scale
READING_FIXED_WEIGHT = -1290696 #what the scale reads with known weight on scale (raw value)
Conv_Ratio = KNOWN_WEIGHT_LBS/READING_FIXED_WEIGHT

# CONSTANTS
EMPTY_WEIGHT_LBS = 30
FULL_WEIGHT_LBS = 160
OZ_PER_LB = 16
OZ_PER_UNIT = 12


# set scale ratio for particular channel and gain which is
# used to calculate the conversion to units. Required argument is only
# scale ratio. Without arguments 'channel' and 'gain_A' it sets
# the ratio for current channel and gain.

ratio = float(READING_FIXED_WEIGHT) / float(KNOWN_WEIGHT_LBS)  # calculate the ratio for channel A and gain 128
hx.set_scale_ratio(ratio)  # set ratio for current channel

def get_reading():
    return hx.get_weight_mean(30) - OFFSET*Conv_Ratio

def get_remaining_weight_lbs():
    weight = get_reading()
    return round(weight - EMPTY_WEIGHT_LBS,2)
    
def get_status_remaining():
    weight_lbs = get_remaining_weight_lbs()
    level_percent = round((weight_lbs / (FULL_WEIGHT_LBS - EMPTY_WEIGHT_LBS))*100,1)
    units_remain = round((weight_lbs*OZ_PER_LB / OZ_PER_UNIT),2)
    return {'weight_lbs':weight_lbs, 'level_percent':level_percent, 'units_remain':units_remain}
