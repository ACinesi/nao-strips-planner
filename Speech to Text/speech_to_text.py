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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
print "Testing internet...."
hostname = "google.it"
response = system("ping " + hostname)

if response == 0:
    print "I can reach internet, I'm going to use Google TTS API"
else:
    print "I can't reach internet, I'm going to use PocketSphinx"

r = sr.Recognizer()  # obtain audio from the microphone
with sr.Microphone() as source:
    print("Please wait 5s. Calibrating microphone...")
    # listen for 5 seconds and create the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=5)
    print("Say something!")
    audio = r.listen(source)

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

print "Processed text", text

root = Node("root")
dare = Node("dare")
prendere = Node("prendere")
palla = Node("palla", True, "!Bring(Ball)")
palla2 = Node("palla", True, "Bring(Ball)")

root.add_child(dare)
root.add_child(prendere)
dare.add_child(palla)
prendere.add_child(palla2)

currentNode = root

for word in text:
    for children in currentNode.children:
        if word == children.name:
            currentNode = children
            break

if currentNode.leaf:
    print "Goal state", currentNode.goal
else:
    raise Exception("No goal reached.")
