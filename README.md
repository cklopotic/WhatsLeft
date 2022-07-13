# :beer: WhatsLeft :beer:
Simple module to take in a reading from a digital scale, and determine how much beer you have left in the keg.

This has a small 2.8" TFT display attached to a Raspberry Pi, along with a digital scale with some load sensors.  This will weigh your half barrel of beer and estimate how much beer you have remaining in your keg.

I embedded the dislay into the tapper handle so you can monitor your keg with every pour.

## To Install and use
1)  Clone this Respository
2)  Install the following two(three) support packages for the Display and the Scale
    - `pip install Adafruit-Blinka`
    - `pip3 install adafruit-circuitpython-rgb-display`
    - 
    - This install gave me troubles with the linking of the import, so I copied the one file to this repo
    - `pip3 install 'git+https://github.com/gandalf15/HX711.git#egg=HX711&subdirectory=HX711_Python3'`
