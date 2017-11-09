import argparse
import time
import strips_planning

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
    my_broker = ALBroker(
        "myBroker",
        "0.0.0.0",  # listen to anyone
        0,  # find a free port and use it
        args.ip,  # parent broker IP
        args.port)  # parent broker port
    print "ALBroker successfully started."
    print "Use Ctrl+c to stop this script       ."
    nao = Nao()
    file = open("strips_nao_example.txt", "r")
    new_file = open("strips_nao_test.txt","w")
    #Inizializzo il file strips per ottenere il piano
    for index,line in enumerate(file.readlines()):
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
            new_file.write(init_state_line+"\n")
        elif index == 1:
            goal_state_line = "Da ricevere dallo speech text"
            print "Line 1: " + goal_state_line
            new_file.write(line)
        else:
            new_file.write(line)
    new_file.flush()
    new_file.close()
    file.flush()
    file.close()

if __name__ == "__main__":
    main()
