
import Display
import time
import Scale


stats = Scale.get_status_remaining()
background = Display.setup()

DEMO = False
temp=100

while True:
	if DEMO:
		temp -= .66
		if (temp < 0):
			temp = 100
		Display.update(background, round(temp*1.3,1), round(temp,1), round(temp*1.77,1))
	else:		
		stats = Scale.get_status_remaining()
		print(stats)
		Display.update(background, stats['weight_lbs'], stats['level_percent'], stats['units_remain'])
	time.sleep(.5)
