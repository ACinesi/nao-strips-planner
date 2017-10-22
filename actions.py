
from naoqi import ALProxy
import sys



'''VARIABLES
'''

safetyDistance=0.3 #Tangential security distance is 0.1 cm (default) 
robotIP=""
PORT=0
#ogni volta la funzione relativa al comando che sta eseguendo sovrascrive argsToSend[0], argsToSend[1], ...
argsToSend=[]

#serve una sincronizzazione, non può eseguire moveTo prima di track
ready=False

'''TRACKING
'''
def track(args):
    ready = False

    print args[0]
    print args[2]

    #alla fine dovrà fare 
    ready=True


    
'''	MOTION

    notions:
    x – Distance along the X axis in meters.
    y – Distance along the Y axis in meters.
    theta – Rotation around the Z axis in radians [-3.1415 to 3.1415].
    void ALMotionProxy::moveTo(const float& x, const float& y, const float& theta)
'''
def moveTo(args):
    ready= False
    try:
        motion = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
    try:
        tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ",e
        
    try:

        motion.stiffnesses(1.0) 
        motion.moveInit()
        tts.say("mi muovo")
        id = motion.post.moveTo(args[0]-safetyDistance, args[1]-safetyDistance, args[3])
        motion.wait(id,0)
        tts.say("sono arrivato")
        ready = True
    except Exception,e:
        print "Something's wrong :/"
        print "Error was: ",e






''' SWITCHER 
'''
def mySwitcher(argument,arg):
    switcher = {
        'track': track,
        'move': moveTo,
        
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument)
    # Execute the function
    ready = False #per sicurezza prima di invocare le funzioni relative ai comandi
    func(arg)


'''

'''



''' MAIN 
'''
def main(): 

    robotIP= sys.argv[1] 
    PORT= sys.argv[2]

    try:
         tts = ALProxy("ALTextToSpeech", robotIP, PORT)
         
    except Exception,e:
        print "Could not create a connection, check the arguments: "+sys.argv[0]+" [IP] [PORT]"
        print "Error was: ",e
        sys.exit()

    tts.say("Ciao a tutti")
      

    while True :
        tts.say("che cosa vuoi?")
        #LISTEN the command
        #TRANSLATE the command  
        commands = ['track','move'] #generati da STRIPS
        #SEND the command
        i=0
        while i==len(commands):
            mySwitcher(commands[i],argsToSend)
            #serve una sincronizzazione con la fine del comando (non penso che mySwitcher aspetti la fine delle funzioni che invoca)
            while ready==False : 
                pass
            i+=1


        



if __name__ == "__main__":
    main()
