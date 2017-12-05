import argparse
from colorama import init, Fore, Back, Style
import time
import traceback
import strips_planning as sp
import speech_to_text as stt
import text_tagger as tt
from naoqi import ALBroker, ALModule, ALProxy
from nao import Nao

nao=None

def main():
    """A simple main"""
    parser = argparse.ArgumentParser()
    # Ottengo da terminale ip e porta
    parser.add_argument(
        "--ip",
        type=str,
        default="192.168.11.3",
        help="Robot IP address. On robot or Local Naoqi: use '192.168.11.3'.")
    parser.add_argument(
        "--port", type=int, default=9559, help="Naoqi port number")
    args = parser.parse_args()
    # Instanzio Nao, la connessione avviene automaticamente
    global nao
    nao = Nao(args.ip, args.port)
    nao.hello()
    # Inizializzo il microfono
    print Fore.GREEN + "### INIT SPEECH-TO-TEXT ###"
    print Style.RESET_ALL
    stt.init()
    # Apro un file strips di riferimento e quello che poi utlizzer per il planner
    # Inizio la routine: ascolto comando-> ottengo il piano -> eseguo il piano
    while True:
        print Fore.GREEN + "### SESSION ###"
        print Style.RESET_ALL
        source_strips = open("strips_nao_example.txt", "r")
        my_strips = open("strips_nao_test.txt", "w")
        # Inizializzo il file strips con Initial State e Goal State
        for index, line in enumerate(source_strips.readlines()):
            if index == 0:
                init_state_line = "Initial state: At(A)"
                posture = nao.get_posture()
                if posture == "Standing":
                    # potrebbe essere anche in un altra posizione
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
                print (Fore.GREEN + "### SPEECH_TO_TEXT ###")
                print(Style.RESET_ALL)
                error = True
                while error:
                    error = False
                    try:
                        speech = stt.listen()
                    except Exception as e:
                        print "Something was wrong with speech recognizing.Retrying.."
                        error = True
                #speech = "prendi la palla"
                print Fore.GREEN + "### TEXT ANALYSIS ###"
                print Style.RESET_ALL
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
        # Ottengo il piano(lista di stringhe)
        print Fore.GREEN + "### STRIPS_PLANNER ###"
        print Style.RESET_ALL
        plan = sp.main()
        print Fore.GREEN + "### NAO CLASS ###"
        print Style.RESET_ALL
        # elaborare il piano ()
        try:
            if plan != None:
                for command in plan:
                    caratteri = list(command)
                    count = 0
                    for x in caratteri:
                        if x != "(":
                            count += 1
                        else:
                            break
                    # invoca un comando alla volta
                    nao.switcher(command[:count])
            else:
                pass

        except KeyboardInterrupt:
            print
            print "Interrupted by user"
            print "Stopping..."
            nao.disconnect()
        finally:
            print Fore.GREEN + "### END SESSION ###"
            print "\n"
            print Style.RESET_ALL


if __name__ == "__main__":
    try:
        init()
        main()
    except IOError as e:
        traceback.print_exc()
