import argparse
import pprint
import time

import qi


class Nao(object):
    def __init__(self, session):
        self.session = session

    def get_posture(self):
        posture_service = session.service("ALRobotPosture")
        posture = posture_service.getPosture()
        return posture

    def go_to_posture(self, posture_name):
        posture_service = session.service("ALRobotPosture")
        result = posture_service.goToPosture(posture_name, 1.0)
        return result

    def hand_full(self):
        motion_service = session.service("ALMotion")
        motion_service.setAngles("LHand", 0.0, 0.25)
        time.sleep(2.0)
        hand_angle = motion_service.getAngles("LHand", True)
        if hand_angle < 0.25:
            result = False
        else:
            result = True
        return result


parser = argparse.ArgumentParser()
parser.add_argument(
    "--ip",
    type=str,
    default="127.0.0.1",
    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
parser.add_argument("--port", type=int, default=9559, help="Naoqi port number")

args = parser.parse_args()
session = qi.Session()
session.connect("tcp://" + args.ip + ":" + str(args.port))

#tts_proxy = session.service("ALTextToSpeech")

nao = Nao(session)

print nao.hand_full()
