import argparse
import time
import math
from naoqi import ALBroker, ALModule, ALProxy


nao = None
FRAME_TORSO = 0
FRAME_ROBOT = 2


class Nao(ALModule):
    """Basic class for interaction to NAO Robot"""

    def __init__(self, ip, port, name="nao"):
        self.my_broker = ALBroker(
            "myBroker",
            "0.0.0.0",  # listen to anyone
            0,  # find a free port and use it
            ip,  # parent broker IP
            port)  # parent broker port
        ALModule.__init__(self, name)
        self.name = name
        self.hand_full_threshold = 0.20
        self.tts_service = ALProxy("ALTextToSpeech")
        self.memory_service = ALProxy("ALMemory")
        self.not_touched = True
        self.not_detected = True

    def hello(self):
        self.tts_service.say("Dai iniziamo!")

    def get_posture(self):
        """Get current NAO posture"""
        posture_service = ALProxy("ALRobotPosture")
        posture = posture_service.getPostureFamily()
        print posture
        return posture

    def go_to_posture(self, posture_name):
        """Make NAO assume a desired posture"""
        posture_service = ALProxy("ALRobotPosture")
        result = posture_service.goToPosture(posture_name, 0.5)
        return result

    def hand_full(self):
        """Check if the right hand is full,grasping something"""
        motion_service = ALProxy("ALMotion")
        motion_service.setAngles("RHand", 0.0, 0.35)
        time.sleep(2.0)
        hand_angle = motion_service.getAngles("RHand", True)
        print hand_angle
        # calibrare il valore in base alla palla
        if hand_angle[0] < self.hand_full_threshold:
            result = False
            #self.tts_service.say("Non ho nulla in mano")
        else:
            #self.tts_service.say("Ho la mano occupata")
            result = True
        return result

    # Actions
    def move(self, destination):
        """Move NAO to a position relative to NAO frame"""
        x = destination[0]
        y = destination[1]
        # TODO  # nel caso ci vengano fornite solo x e y senza theta
        theta = math.atan(y / x)
        motion_service = ALProxy("ALMotion")
        motion_service.moveInit()
        motion_service.moveTo(x, y, theta)
        self.tts_service.say("Sono arrivata")

    def take_ball(self):
        """Make NAO capable of taking a red ball (Touch the hand after putting the ball on its hand)"""
        """LAST IMPROVEMENT: NAO follow the ball with the head"""
        """TODO: NAO recognize to have the ball without touching the hand"""
        print "takeball"
        names = ["RShoulderPitch", "RWristYaw", "RElbowYaw", "RHand"]
        angles = [0.441, 1.815,1.335 ,1.00]
        fraction_max_speed = 0.2
        self.wait_redball()
        #self.tts_service.say("Vedo la palla")
        self.redball_follower(True)
        #time.sleep(2.0)
        motion_service = ALProxy("ALMotion")
        motion_service.setStiffnesses("RArm", 1.0)
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(1.0)
        self.memory_service.subscribeToEvent("HandRightBackTouched", self.name,
                                             "hand_touched")
        while self.not_touched:
            pass
            #time.sleep(1.0)
            # self.memory_service.raiseEvent("MiddleTactilTouched", 1.0)
        self.not_touched = True
        self.redball_follower(False)
        motion_service.setAngles("RHand", 0.00, 0.25)
        time.sleep(2.0)
        names = names[0:3]
        angles = [1.47, 0.11, 1.20]
        motion_service.setAngles(names, angles, fraction_max_speed)
        #time.sleep(2.0)
        #motion_service.setStiffnesses("RArm", 0.0)

    def give_ball(self):
        """Make NAO capable of giving a red ball (Touch the hand after taking the ball on its hand)"""
        names = ["RShoulderPitch", "RWristYaw", "RElbowYaw"]
        angles = [0.441, 1.815,1.335]
        fraction_max_speed = 0.2
        motion_service = ALProxy("ALMotion")
        motion_service.setStiffnesses("RArm", 1.0)
        motion_service.setAngles(names, angles, fraction_max_speed)
        time.sleep(2.0)
        motion_service.setAngles("RHand", 1.00, fraction_max_speed)
        self.memory_service.subscribeToEvent("HandRightBackTouched", self.name,
                                             "hand_touched")
        self.not_touched=True
        while self.not_touched:
            #pass
            time.sleep(1.0)
            # self.memory_service.raiseEvent("MiddleTactilTouched", 1.0)
        self.not_touched = True
        self.go_to_posture("Stand")

    def wait_redball(self):
        """Make NAO wait until it detect a red ball"""
        self.memory_service.subscribeToEvent("redBallDetected", self.name,
                                             "redball_detected")
        #self.tts_service.say("Mostrami la palla")
        while self.not_detected:
            pass
            #time.sleep(1.0)
        self.not_detected = False

    def redball_follower(self, start, mode="Head"):
        """Make NAO track a redball using mode selected"""
        tracker = ALProxy("ALTracker")
        motion_service = ALProxy("ALMotion")
        motion_service.wakeUp()
        self.go_to_posture("Stand")
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

    # def redball_follower_1(self, start, mode="Head"):
    #     #TODO check estimation error of the ball position respect to the hand(through the camera)
    #     """Make NAO track a redball using mode selected"""
    #     names = ["RShoulderPitch", "RWristYaw", "RElbowYaw", "RHand"]
    #     angles = [0.26, 1.22, 1.74, 1.00]
    #     fraction_max_speed = 0.2
    #     tracker = ALProxy("ALTracker")
    #     motion_service = ALProxy("ALMotion")
    #     motion_service.wakeUp()
    #     self.go_to_posture("Stand")
    #     motion_service.setStiffnesses("RArm", 1.0)
    #     motion_service.setAngles(names, angles, fraction_max_speed)
    #     time.sleep(2.0)
    #     if start:
    #         target_name = "RedBall"
    #         diameter_ball = 0.04  # da controllare
    #         tracker.registerTarget("target_name", diameter_ball)
    #         tracker.setMode(mode)
    #         tracker.setEffector("None")
    #         tracker.track(target_name)
    #         ball_position = tracker.getTargetPosition(2)
    #         hand_position = motion_service.getPosition("RHand", 0, False)
    #         try:
    #             while True:
    #                 ball_position = tracker.getTargetPosition(2)
    #                 diff_x = ball_position[0] - hand_position[0]
    #                 diff_y = ball_position[1] - hand_position[1]
    #                 diff_z = ball_position[2] - hand_position[2]
    #                 print "Error estimated: " + str(ball_position[0]) + " " + str(ball_position[1]) + " " + str(ball_position[2])
    #                 time.sleep(2.0)
    #         except KeyboardInterrupt:
    #             print
    #             print "Interrupted by user"
    #             print "Stopping..."
    #         finally:
    #             tracker.stopTracker()
    #             tracker.unregisterAllTargets()
    #     else:
    #         tracker.stopTracker()
    #         tracker.unregisterAllTargets()

    def find_person(self):
        """Make NAO find a person position given the target name"""
        # name is always Face
        #mode is Move
        tracker = ALProxy("ALTracker")
        target_name = "Face"
        face_width = 0.14
        tracker.registerTarget(target_name, face_width)
        tracker.setMode("Move")
        tracker.setEffector("None")
        tracker.track(target_name)
        too_far = True
        #tracker.toggleSearch(True)
        while too_far:
            position = tracker.getTargetPosition(FRAME_ROBOT)
            if position != []:
                distance = math.sqrt(position[0]**2 + position[1]**2)
                print distance
                print position
                if distance < 0.50:
                    too_far = False
                    tracker.stopTracker()
                    tracker.unregisterAllTargets()
                    print "Target reached"
        too_far=True
        self.tts_service.say("Eccomi qua!")

    def find_ball(self):
        """Make NAO find a ball"""
        tracker = ALProxy("ALTracker")
        target_name = "RedBall"
        diameter_ball = 0.04 #0.04
        tracker.registerTarget(target_name, diameter_ball)
        tracker.setMode("Move")
        tracker.setEffector("None")
        tracker.track(target_name)
        self.tts_service.say("Mostrami la palla")
        too_far = True
        #tracker.toggleSearch(True)
        while too_far:
            position = tracker.getTargetPosition(FRAME_ROBOT)
            if position != []:
                distance = math.sqrt(math.pow(position[0],2) + math.pow(position[1],2))
                print position
                print distance
                if distance < 0.25: #0.50
                    too_far = False
                    tracker.stopTracker()
                    tracker.unregisterAllTargets()
                    print "Target reached"
        too_far=True
        time.sleep(1.0)
        self.tts_service.say("Trovata")

        


# Callback

    def redball_detected(self, event_name, value):
        """Callback method for redBallDetected event"""
        print "Event raised: " + event_name + " " + str(value)
        self.memory_service.unsubscribeToEvent("redBallDetected", self.name)
        self.not_detected = False

    def hand_touched(self, event_name, value):
        """Callback method for HandRightBackTouched event"""
        print "Event raised: " + event_name + " " + str(value)
        self.memory_service.unsubscribeToEvent("HandRightBackTouched",
                                               self.name)
        self.not_touched = False

    def disconnect(self):
        self.my_broker.shutdown()
        print "Disconnecting...."

    def switcher(self,function):
        switcher = { 'TakeBall': self.take_ball, 'GiveBall':self.give_ball,'FindPerson': self.find_person ,'FindBall':self.find_ball}
        result=None
        # Get the function from switcher dictionary
        func = switcher.get(function)
        if func != None:
            # Execute the function
            result = func()
     
        return result




def main():
    """A simple main"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.11.3",
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.11.3'.")
    parser.add_argument(
        "--port", type=int, default=9559, help="Naoqi port number")
    args = parser.parse_args()
    global nao
    nao = Nao(args.ip, args.port)
    try:
        nao.redball(False)
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."
    finally:
        nao.disconnect()


if __name__ == "__main__":
    main()
