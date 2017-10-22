# -*- encoding: UTF-8 -*-

import time
import argparse
import math
from naoqi import ALProxy

IP = "127.0.0.1"
PORT = 49247

motionProxy = ALProxy("ALMotion", IP, PORT)
trackerProxy = ALProxy("ALTracker", IP, PORT)
motionProxy.setStiffnesses("Head", 1.0)
# Example showing a slow, relative move of "HeadYaw".
# Calling this multiple times will move the head further.
names = "HeadYaw"
step = 0.25
fractionMaxSpeed = 0.05

# Add target to track.
targetName = "Enrico"  # To receive as a parameter
faceWidth = 123  # Where to find it?? TODO
trackerProxy.registerTarget(targetName, faceWidth)
# Then, start tracker.
trackerProxy.track(targetName)
print "Start tracking..."
currentAngle = [0.0]
dirChange = 0
found = False
# Set head to default position
motionProxy.setAngles(names, 0.0, fractionMaxSpeed)
motionProxy.setAngles("HeadPitch", -0.35, fractionMaxSpeed)
print "Moving head to default position..."
while motionProxy.getAngles(names, True)[0] != 0.0:
    pass

while dirChange != 2 and not found:
    motionProxy.changeAngles(names, step, fractionMaxSpeed)
    while motionProxy.getAngles(names, True)[0] != currentAngle[0] + step:
        pass
    time.sleep(2.0)
    # Get current target position
    position = trackerProxy.getTargetPosition(2)
    if position != []:
        found = True
        print "Target found at position " + position

    currentAngle = motionProxy.getAngles(names, True)
    print "Head yaw: "
    print currentAngle
    if abs(currentAngle[0]) == 2.0:
        step = -step
        dirChange += 1
        motionProxy.setAngles(names, 0.0, fractionMaxSpeed)
        while motionProxy.getAngles(names, True)[0] != 0.0:
            pass
        currentAngle = motionProxy.getAngles(names, True)


# Stop tracker.
trackerProxy.stopTracker()
trackerProxy.unregisterAllTargets()
# Return head to default position
motionProxy.setAngles(names, 0, fractionMaxSpeed)
while motionProxy.getAngles(names, True)[0] != 0.0:
    pass
motionProxy.setStiffnesses("Head", 0.0)

if not found:
    print "Target not found,aborting....."
