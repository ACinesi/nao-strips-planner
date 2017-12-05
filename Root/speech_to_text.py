import speech_recognition as sr
import socket
import text_tagger as tt
from os import system

r = None
m = None
response = None


def init():
    # Create a TCP / IP socket
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Testing internet...."
    hostname = "google.it"
    global response
    #response = system("ping " + hostname)
    response = 0
    if response == 0:
        print "I can reach internet, I'm going to use Google TTS API"
    else:
        print "I can't reach internet, I'm going to use PocketSphinx"
    global r, m
    r = sr.Recognizer()  # obtain audio from the microphone
    m = sr.Microphone()


def listen():
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
    return speech


def main():
    init()
    listen()


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
