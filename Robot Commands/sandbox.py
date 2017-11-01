import naoqi as qi
import argparse
import qi

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
