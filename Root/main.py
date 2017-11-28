import argparse
import time
import strips_planning as sp
import speech_to_text as stt
import text_tagger as tt
from naoqi import ALBroker, ALModule, ALProxy
from nao import Nao


def main():
    """A simple main"""
    parser = argparse.ArgumentParser()
    # Ottengo da terminale ip e porta
    parser.add_argument(
        "--ip",
        type=str,
        default="127.0.0.1",
        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument(
        "--port", type=int, default=9559, help="Naoqi port number")
    args = parser.parse_args()
    # Instanzio Nao, la connessione avviene automaticamente
    nao = Nao(args.ip, args.port)
    #Inizializzo il microfono
    print "### INIT SPEECH-TO-TEXT ###"
    stt.init()
    # Apro un file strips di riferimento e quello che poi utlizzer per il planner
    
    # Inizio la routine: ascolto comando-> ottengo il piano -> eseguo il piano
    while True:
        print "### SESSION ###"
        source_strips = open("strips_nao_example.txt", "r")
        my_strips = open("strips_nao_test.txt", "w")
        # Inizializzo il file strips con Initial State e Goal State
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
                print init_state_line
                my_strips.write(init_state_line + "\n")
            elif index == 1:
                print "### SPEECH_TO_TEXT ###"
                error = True
                while error:
                    error = False
                    try:
                        speech = stt.listen()
                    except Exception as e:
                        print "Something was wrong with speech recognizing.Retrying...."  
                        error = True  
                #speech = "prendi la palla"
                print "### TEXT ANALYSIS ###"
                goals = tt.strips_goals(speech)
                goal_state_line = "Goal state: "
                if goals != "":
                    goal_state_line += goals
                print goal_state_line
                my_strips.write(goal_state_line)
            else:
                my_strips.write(line)

        my_strips.flush()
        source_strips.flush()
        my_strips.close()
        source_strips.close()
        time.sleep(1)
        # Ottengo il piano(lista di stringhe)
        print "### STRIPS_PLANNER ###"
        plan = sp.main()
        print "\n"

    nao.disconnect()


if __name__ == "__main__":
    main()
