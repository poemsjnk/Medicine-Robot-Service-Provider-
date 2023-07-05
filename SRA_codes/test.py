import time
import random

from loadjsonintents import load_json_intents
# the order of imports are important
# import libpath
import sys
sys.path.append("../lib")

from naoqi import ALProxy, ALModule, ALBroker

from speechdetectmod import SpeechDetectionModule

ip = "172.20.10.2"
port = 9559

myBroker = ALBroker("NaoAppBroker",
		"0.0.0.0",   # listen to anyone
		0,           # find a free port and use it
		ip,      # parent broker IP
		port)    # parent broker port


tts = ALProxy("ALTextToSpeech", ip, port)
tts.setVolume(0.5)

myBroker.shutdown()