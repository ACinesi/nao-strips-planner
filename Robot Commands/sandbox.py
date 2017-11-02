import argparse
import pprint
import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

Nao = None
memory_service = None
not_touched = True


class Nao(ALModule):
    def __init__(self, name="Nao"):
        ALModule.__init__(self, name)
        self.name = name
        self.hand_full_threshold = 0.25
        self.tts_service = ALProxy("ALTextToSpeech")

    def get_posture(self):
        posture_service = ALProxy("ALRobotPosture")
        posture = posture_service.getPosture()
        return posture

    def go_to_posture(self, posture_name):
        posture_service = ALProxy("ALRobotPosture")
        result = posture_service.goToPosture(posture_name, 1.0)
        return result

    def hand_full(self):
        motion_service = ALProxy("ALMotion")
        motion_service.setAngles("RHand", 0.0, 0.25)
        time.sleep(2.0)
        hand_angle = motion_service.getAngles("RHand", True)
        print hand_angle
        if hand_angle[0] < self.hand_full_threshold:  #calibrare il valore in base alla palla
            result = False
        else:
            result = True
        return result

    #Actions
    def move(self, destination):
        x = destination[0]
        y = destination[1]
        #theta=math.pi/2 se ci vengono fornite solo x e y
        theta = destination[2]
        motion_service = ALProxy("ALMotion")
        motion_service.moveInit()
        motion_service.moveTo(x, y, theta)
        self.tts_service.say("Sono arrivata")

    def take_ball(self):
        names = ["RShoulderPitch", "RWristYaw", "RElbowYaw", "RHand"]
        angles = [0.26, 1.22, 1.74, 1.00]
        fraction_max_speed = 0.2
        motion_service = ALProxy("ALMotion")
        motion_service.setStiffnesses("RArm", 1.0)
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(2.0)
        self.tts_service.say("Sono pronta")
        global memory_service
        memory_service = ALProxy("ALMemory")
        memory_service.subscribeToEvent("MiddleTactilTouched", self.name,
                                        "head_touched")
        global not_touched
        while not_touched:
            time.sleep(4.0)
            memory_service.raiseEvent("MiddleTactilTouched", 1.0)
        not_touched = True
        motion_service.setAngles("RHand", 0.00, fraction_max_speed)
        time.sleep(1.0)
        names = names[0:3]
        angles = [1.47, 0.11, 1.20]
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(2.0)
        motion_service.setStiffnesses("RArm", 0.0)

    def give_ball(self):
        names = ["RShoulderPitch", "RWristYaw", "RElbowYaw"]
        angles = [0.26, 1.22, 1.74]
        fraction_max_speed = 0.2
        motion_service = ALProxy("ALMotion")
        motion_service.setStiffnesses("RArm", 1.0)
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(2.0)
        motion_service.setAngles("RHand", 1.00, fraction_max_speed)
        time.sleep(1.0)
        global memory_service
        memory_service = ALProxy("ALMemory")
        memory_service.subscribeToEvent("MiddleTactilTouched", self.name,
                                        "head_touched")
        global not_touched
        while not_touched:
            time.sleep(4.0)
            memory_service.raiseEvent("MiddleTactilTouched", 1.0)
        not_touched = True
        self.go_to_posture("Stand")

    def head_touched(self, val, sub_id):
        global memory_service
        memory_service.unsubscribeToEvent("MiddleTactilTouched", self.name)
        global not_touched
        not_touched = False


parser = argparse.ArgumentParser()
parser.add_argument(
    "--ip",
    type=str,
    default="127.0.0.1",
    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
parser.add_argument("--port", type=int, default=9559, help="Naoqi port number")

args = parser.parse_args()
#Da portare nella classe Nao in init
myBroker = ALBroker(
    "myBroker",
    "0.0.0.0",  # listen to anyone
    0,  # find a free port and use it
    args.ip,  # parent broker IP
    args.port)  # parent broker port

#tts_proxy = session.service("ALTextToSpeech")
global Nao
Nao = Nao()
Nao.go_to_posture("Stand")
Nao.give_ball()
myBroker.shutdown()