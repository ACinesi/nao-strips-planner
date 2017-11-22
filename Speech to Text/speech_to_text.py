import speech_recognition as sr
import socket
import text_tagger as tt
from os import system


class Node(object):
    def __init__(self, name, leaf=False, goal=None):
        self.name = name
        self.children = []
        self.leaf = leaf
        self.goal = goal

    def add_child(self, obj):
        self.children.append(obj)


def listen_commands():
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Testing internet...."
    hostname = "google.it"
    response = system("ping " + hostname)

    if response == 0:
        print "I can reach internet, I'm going to use Google TTS API"
    else:
        print "I can't reach internet, I'm going to use PocketSphinx"

    r = sr.Recognizer()  # obtain audio from the microphone
    m = sr.Microphone()
    with m as source:
        print("Please wait 5s. Calibrating microphone...")
        # listen for 5 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=5)
        print("Say something!")
        audio = r.listen(source, 5, 5)

    try:  # recognize speech using Sphinx or Google TTS API
        if response == 0:
            speech = r.recognize_google(audio, None, "it-IT")
        else:
            speech = r.recognize_sphinx(audio, "it-IT")
        print("I think you said '" + speech + "'")
    except sr.UnknownValueError:
        print("I could not understand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))

    text = tt.process_text(speech)

    print "Processed text->", text

    root = Node("root")
    dare = Node("dare")
    prendere = Node("prendere")
    trovare = Node("trovare")
    palla = Node("palla", True, "!Bring(Ball)")
    palla2 = Node("palla", True, "Bring(Ball)")
    enrico = Node("enrico", True, "PersonAt(enrico,B),At(B)")

    root.add_child(dare)
    root.add_child(prendere)
    root.add_child(trovare)
    dare.add_child(palla)
    prendere.add_child(palla2)
    trovare.add_child(enrico)

    goals = list()
    currentNode = root
    for word in text:
        for children in currentNode.children:
            if word == children.name:
                if children.leaf:
                    goals.append(children.goal)
                    currentNode = root
                else:
                    currentNode = children

    if len(goals) > 0:
        for goal in goals:
            print "Goal state->", goal
    else:
        raise Exception("No goal reached.")


def main():
    listen_commands()


if __name__ == '__main__':
    main()

# recognized = False
# # this is called from the background thread
# def callback(recognizer, audio):
#     # received audio data, now we'll recognize it using Google Speech Recognition
#     try:
#         # for testing purposes, we're just using the default API key
#         # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#         # instead of `r.recognize_google(audio)`
#         text=recognizer.recognize_google(audio, None, "it-IT")
#         if(text=="ferma"):
#             global recognized
#             recognized=True
#         print("Google Speech Recognition thinks you said " + text)
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))
# stop_listening = r.listen_in_background(m, callback,2)
# while not recognized:
#     time.sleep(1.0)
