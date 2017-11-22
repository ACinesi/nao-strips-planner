import argparse
import time
import math
from naoqi import ALBroker, ALModule, ALProxy

nao = None
FRAME_TORSO = 0


class Nao(ALModule):
    """Basic class for interaction to NAO Robot"""

    def __init__(self, name="nao"):
        ALModule.__init__(self, name)
        self.name = name
        self.hand_full_threshold = 0.25
        self.tts_service = ALProxy("ALTextToSpeech")
        self.memory_service = ALProxy("ALMemory")
        self.not_touched = True
        self.not_detected = True

    def get_posture(self):
        """Get current NAO posture"""
        posture_service = ALProxy("ALRobotPosture")
        posture = posture_service.getPosture()
        return posture

    def go_to_posture(self, posture_name):
        """Make NAO assume a desired posture"""
        posture_service = ALProxy("ALRobotPosture")
        result = posture_service.goToPosture(posture_name, 1.0)
        return result

    def hand_full(self):
        """Check if the right hand is full,grasping something"""
        motion_service = ALProxy("ALMotion")
        motion_service.setAngles("RHand", 0.0, 0.25)
        time.sleep(2.0)
        hand_angle = motion_service.getAngles("RHand", True)
        print hand_angle
        # calibrare il valore in base alla palla
        if hand_angle[0] < self.hand_full_threshold:
            result = False
            self.tts_service.say("Non ho nulla in mano")
        else:
            self.tts_service.say("Ho la mano occupata")
            result = True
        return result

    # Actions
    def move(self, destination):
        """Move NAO to a position relative to NAO frame"""
        x = destination[0]
        y = destination[1]
        theta = math.pi / 2  # nel caso ci vengano fornite solo x e y senza theta
        motion_service = ALProxy("ALMotion")
        motion_service.moveInit()
        motion_service.moveTo(x, y, 0.0)
        self.tts_service.say("Sono arrivata")

    def take_ball(self):
        """Make NAO capable of taking a red ball (Touch the head after putting the ball on its hand)"""
        """LAST IMPROVEMENT: NAO follow the ball with the head"""
        """TODO: NAO recognize to have the ball without touching the head"""
        names = ["RShoulderPitch", "RWristYaw", "RElbowYaw", "RHand"]
        angles = [0.26, 1.22, 1.74, 1.00]
        fraction_max_speed = 0.2
        self.wait_redball()
        self.tts_service.say("Vedo la palla")
        self.redball_follower(True)
        time.sleep(2.0)
        motion_service = ALProxy("ALMotion")
        motion_service.setStiffnesses("RArm", 1.0)
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(2.0)
        self.memory_service.subscribeToEvent("MiddleTactilTouched", self.name,
                                             "head_touched")
        while self.not_touched:
            time.sleep(2.0)
            #self.memory_service.raiseEvent("MiddleTactilTouched", 1.0)
        self.not_touched = True
        self.redball_follower(False)
        motion_service.setAngles("RHand", 0.00, fraction_max_speed)
        time.sleep(1.0)
        names = names[0:3]
        angles = [1.47, 0.11, 1.20]
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(2.0)
        motion_service.setStiffnesses("RArm", 0.0)

    def give_ball(self):
        """Make NAO capable of giving a red ball (Touch the head after taking the ball on its hand)"""
        names = ["RShoulderPitch", "RWristYaw", "RElbowYaw"]
        angles = [0.26, 1.22, 1.74]
        fraction_max_speed = 0.2
        motion_service = ALProxy("ALMotion")
        motion_service.setStiffnesses("RArm", 1.0)
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(2.0)
        motion_service.setAngles("RHand", 1.00, fraction_max_speed)
        time.sleep(1.0)
        self.memory_service.subscribeToEvent("MiddleTactilTouched", self.name,
                                             "head_touched")
        while self.not_touched:
            time.sleep(1.0)
            #self.memory_service.raiseEvent("MiddleTactilTouched", 1.0)
        self.not_touched = True
        self.go_to_posture("Stand")

    def wait_redball(self):
        """Make NAO wait until it detect a red ball"""
        self.memory_service.subscribeToEvent("redBallDetected", self.name,
                                             "redball_detected")
        self.tts_service.say("Mostrami la palla")
        while self.not_detected:
            time.sleep(1.0)
            # self.memory_service.raiseEvent("redBallDetected", 1.0)
        self.not_detected = False

    def redball_follower(self, start, mode="Head"):
        """Make NAO track a redball using mode selected"""
        tracker = ALProxy("ALTracker")
        motion_service = ALProxy("ALMotion")
        motion_service.wakeUp()
        self.go_to_posture("StandInit")
        if start:
            target_name = "RedBall"
            diameter_ball = 0.04  # da controllare
            tracker.registerTarget(target_name, diameter_ball)
            tracker.setMode(mode)
            tracker.setEffector("None")
            tracker.track(target_name)
            # while not tracker.isNewTargetDetected():
            #     print "."
            # time.sleep(2.0)
            # position = tracker.getTargetPosition(2)
            # print position
            # tracker.stopTracker()
            # tracker.unregisterAllTargets()
            # return position
        else:
            tracker.stopTracker()
            tracker.unregisterAllTargets()

    def find_person(self, name):
        """Make NAO find a person position given the target name"""
        tracker = ALProxy("ALTracker")
        target_name = name
        face_width = 12
        tracker.registerTarget(name, face_width)
        tracker.setMode("Head")
        tracker.setEffector("None")
        tracker.track(target_name)
        while not tracker.isNewTargetDetected():
            pass
        self.tts_service.say(name + " trovato")
        time.sleep(2.0)
        position = tracker.getTargetPosition(2)
        print "Target " + name + " found at " + position
        tracker.stopTracker()
        tracker.unregisterAllTargets()
        return position


# Callback

    def redball_detected(self, event_name, value):
        """Callback method for redBallDetected event"""
        # motion = ALProxy("ALMotion")
        # pos = motion.getPosition("RHand",0,False)
        # time.sleep(2.0)
        # print pos
        print event_name
        print value
        self.memory_service.unsubscribeToEvent("redBallDetected", self.name)
        self.not_detected = False

    def head_touched(self, event_name, value):
        """Callback method for MiddleTactilTouched event"""
        print "Event raised: " + event_name + " " + str(value)
        self.memory_service.unsubscribeToEvent("MiddleTactilTouched",
                                               self.name)
        self.not_touched = False


def main():
    """A simple main"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        type=str,
        default="127.0.0.1",
        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument(
        "--port", type=int, default=9559, help="Naoqi port number")
    args = parser.parse_args()
    my_broker = ALBroker(
        "myBroker",
        "0.0.0.0",  # listen to anyone
        0,  # find a free port and use it
        args.ip,  # parent broker IP
        args.port)  # parent broker port
    print "ALBroker successfully started."
    print "Use Ctrl+c to stop this script       ."

    try:
        global nao
        nao = Nao()

        print(nao.get_posture())
        print(nao.hand_full())
        
        '''
        nao.take_ball()
        nao.give_ball()
        position = nao.find_person("Enrico")
        time.sleep(2.0)
        nao.move(position)

        '''
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."
    finally:
        my_broker.shutdown()


if __name__ == "__main__":
    main()
