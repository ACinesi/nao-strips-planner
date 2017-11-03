import speech_recognition as sr
import socket
import text_tagger as tt
from os import system

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
        speech = r.recognize_google(audio, None, "en-UK")
    else:
        speech = r.recognize_sphinx(audio, "it-IT")
    print("I think you said '" + speech + "'")
except sr.UnknownValueError:
    print("I could not understand audio")
except sr.RequestError as e:
    print("Error; {0}".format(e))

text = tt.process_text(speech)

print "Processed text", text

# TODO Filter the commands to obtain senteces structured as verbs + noun(or personal noun) (Es. prendere palla, andare enrico)
# use TreeTagger

# class Node(object):
#     def __init__(self, name, leaf=False, goal=None):
#         self.name = name
#         self.children = []
#         self.leaf = leaf
#         self.goal = goal

#     def add_child(self, obj):
#         self.children.append(obj)

# start = Node("start")
# take = Node("take")
# move = Node("move")
# the = Node("the")
# to = Node("to")
# ball = Node("ball", True, "bring(Ball)")
# thomas = Node("thomas", True, "at(Thomas)")

# start.add_child(take)
# start.add_child(move)
# take.add_child(the)
# move.add_child(to)
# the.add_child(ball)
# to.add_child(thomas)

# commands = speech.split(" and ")

# # print command

# for command in commands:
#     words = command.split(" ")
#     # print words
#     currentNode = start
#     for word in words:
#         for children in currentNode.children:
#             if word.lower() == children.name:
#                 currentNode = children
#                 break

#     if currentNode.leaf:
#         print(command + " -> " + currentNode.goal)
#     else:
#         raise Exception("No goal reached.")

# # WORKFLOW
# # extract commands from commands
# # fill the initial state
# # build the goal state
# # update the strips_commands.txt in according to
# # run the strips solver
# # get the plan
# # execute one by one the actions of the plan
