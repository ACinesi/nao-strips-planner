import argparse
import time
import strips_planning as sp
import speech_to_text as stt
from naoqi import ALBroker, ALModule, ALProxy
from nao import Nao


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
    nao = Nao(args.ip, args.port)
    source_strips = open("strips_nao_example.txt", "r")
    my_strips = open("strips_nao_test.txt", "w")
    # Inizializzo il file strips per ottenere il piano
    for index, line in enumerate(source_strips.readlines()):
        if index == 0:
            init_state_line = "Initial state: At(A)"
            posture = nao.get_posture()
            if posture == "Stand":
                posture_line = "Posture(high)"
            else:
                posture_line = "Posture(low)"
            init_state_line = init_state_line + "," + posture_line
            hand_full = nao.hand_full()
            if hand_full:
                hand_line = "Hand(full),Bring(ball)"
            else:
                hand_line = "Hand(empty)"
            init_state_line = init_state_line + "," + hand_line
            print "Line 0: " + init_state_line
            my_strips.write(init_state_line + "\n")
        elif index == 1:
            goals = stt.listen_commands()
            goal_state_line = "Goal state: "
            if goals != "":
                goal_state_line += goals
            print "Line 1: " + goal_state_line
            my_strips.write(line)
        else:
            my_strips.write(line)

    my_strips.flush()
    my_strips.close()
    source_strips.flush()
    source_strips.close()     
    print sp.main()

if __name__ == "__main__":
    main()
