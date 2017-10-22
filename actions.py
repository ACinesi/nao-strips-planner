import sys
import time
import math
from naoqi import ALProxy

safetyDistance = 0.3  # Tangential security distance is 0.1 cm (default)
robotIP = ""
PORT = 0


def track_face(args):
    print "INSIDE track function"
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
        trackerProxy = ALProxy("ALTracker", robotIP, PORT)
    except Exception as exception:
        print "Could not create proxy"
        print "Error was: " + exception.message

    motionProxy.setStiffnesses("Head", 1.0)
    # Example showing a slow, relative move of "HeadYaw".
    # Calling this multiple times will move the head further.
    names = "HeadYaw"
    step = 1.00  # 0.25
    fractionMaxSpeed = 0.05

    # Add target to track.
    targetName = "Enrico"
    faceWidth = 123  # to take as parameter
    trackerProxy.registerTarget(targetName, faceWidth)
    # Then, start tracker.
    trackerProxy.track(targetName)
    print "Start tracking..."
    currentAngle = [0.0]
    dirChange = 0
    found = False
    # Set head to default yaw and change pitch to catch faces
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
        print "Target not found"

    position = [1.0, 1.0, 1.0]
    return position


def move_to(args):
    print "INSIDE move_to function"
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
        ttsProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
    except Exception as exception:
        print "Could not create proxy"
        print "Error was: " + exception.message

    try:
        motionProxy.wakeUp()
        motionProxy.moveInit()
        ttsProxy.say("Mi muovo")
        actionID = motionProxy.post.moveTo(args[0] - safetyDistance,
                                           args[1] - safetyDistance, args[2])
        motionProxy.wait(actionID, 0)
        ttsProxy.say("Sono arrivato")
    except Exception as exception:
        print "Something's wrong :/"
        print "Error was: " + exception.message


def my_switcher(function, arg):
    switcher = {'track': track_face, 'move': move_to}
    # Get the function from switcher dictionary
    func = switcher.get(function)
    # Execute the function
    result = func(arg)
    return result


def main():

    global robotIP
    global PORT

    robotIP = "127.0.0.1"
    PORT = 6048
    print robotIP, PORT

    try:
        tts = ALProxy("ALTextToSpeech", robotIP, PORT)

    except Exception as exception:
        print "Could not create a connection, check the arguments: " + sys.argv[0] + " [IP] [PORT]"
        print "Error was: " + exception.message
        sys.exit()

    tts.say("Ciao a tutti")
    args_to_send = []
    while True:
        tts.say("Cosa devo fare?")
        # LISTEN the speech
        # TRANSLATE the speech to commands
        # GENERATE plans for the commands
        commands = ['track', 'move']  # generati da STRIPS
        # SEND the actions of the current plan
        for command in commands:
            args_to_send = my_switcher(command, args_to_send)


if __name__ == "__main__":
    main()
