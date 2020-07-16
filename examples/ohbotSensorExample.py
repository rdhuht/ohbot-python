from ohbot import ohbot
from time import *
## Example program for using sensors with ohbot.
## Tilt sensor - a3
## Light sensor - a4
## Touch sensor - a5

ohbot.reset()
while True:    

    val1 = ohbot.readSensor(4)  # Tilt
    
    val2 = ohbot.readSensor(3)  # Light

    val3 = ohbot.readSensor(5)  # Touch

    # ohbot.setEyeColour(val2, 10 - val2, 0, True)
    # ohbot.move(ohbot.HEADTURN, val2)
    sleep(0.5)
    print(val3)
    # if val1 > 2:
    #     ohbot.say("put me down")
    #
    # if val2 < 2:
    #     ohbot.say("who turned out the lights")
    #
    # ohbot.wait(0.1)

