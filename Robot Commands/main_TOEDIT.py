import sys
import time
import math
from naoqi import ALProxy


# def my_switcher(function, arg):
#     switcher = {'track': track_face, 'move': move_to}
#     # Get the function from switcher dictionary
#     func = switcher.get(function)
#     # Execute the function
#     result = func(arg)
#     return result


def main():

    global robotIP
    global PORT

    robotIP = "127.0.0.1"
    PORT = 61306
    print robotIP, PORT

    try:
        ttsProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception as exception:
        print "Could not create a connection, check the arguments: " + sys.argv[0] + " [IP] [PORT]"
        print "Error was: " + exception.message
        sys.exit()
    if not motionProxy.robotIsWakeUp():
        actionId = motionProxy.wakeUp()
        motionProxy.wait(actionId, 0)
    ttsProxy.say("Ciao a tutti, sono pronto")
    args_to_send = []
    while True:
        ttsProxy.say("Cosa devo fare?")
        # LISTEN the speech
        # TRANSLATE the speech to commands
        # GENERATE plans for the commands
        commands = ['track', 'move']  # generati da STRIPS
        # SEND the actions of the current plan
        for command in commands:
            args_to_send = my_switcher(command, args_to_send)


if __name__ == "__main__":
    main()
