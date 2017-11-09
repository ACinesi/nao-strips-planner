import argparse
import time

from naoqi import ALBroker, ALModule, ALProxy

from nao import Nao


def main():
    nao = Nao()
    file = open("../Strips Parser/strips_nao_example.txt", "r+")
    #Inizializzo il file strips per ottenere il piano
    for index, _ in enumerate(file.readlines()):
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
            file.write(init_state_line)
        elif index == 1:
            goal_state_line = "Da ricevere dallo speech text"
            print "Line 1: " + goal_state_line
        file.flush()
        file.close()
        plan = 

if __name__ == "__main__":
    main()
