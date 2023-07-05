import time
import random
import sys

from loadjsonintents import load_json_intents
# the order of imports are important
# import libpath
sys.path.append("../lib")

from naoqi import ALProxy, ALModule, ALBroker

from speechdetectmod import SpeechDetectionModule

"""
Convenient function to disable speech recognition while speaking
"""
def speak(text):
	SpeechDetection.asr.pause(True)
	tts.say(text)
	SpeechDetection.asr.pause(False)

# get robot ip
'''
TODO: You need to find out your robot IP address
'''
ip = "172.20.10.2"
port = 9559

# load intents from file and extract a list of all example phrases
intents = load_json_intents("intents.json")
phrases = []
for intent in intents:
	phrases += intent["examples"]
print(phrases)



# setup subsystems
tts = ALProxy("ALTextToSpeech", ip, port)
tts.setVolume(1)

try:
	# this is required to use the ALModule for SpeechDetection
	print("Create an ALBroker")

	myBroker = ALBroker("NaoAppBroker",
		"0.0.0.0",   # listen to anyone
		0,           # find a free port and use it
		ip,      # parent broker IP
		port)    # parent broker port
	SpeechDetection = SpeechDetectionModule("SpeechDetection")

	if SpeechDetection:
		SpeechDetection.setVocabulary(phrases)

	done = False
	speak("Hello, I am Nao. I am your treatment assistant. Speak freely")
	last_hint = time.time()

	while not done:
		if SpeechDetection.detectedPhrase:
			# print(SpeechDetection.detectedPhrase)

			'''
			TODO:
			- Loop over all the intents loaded from intents.json
			- Extract the detected phrase in the handler
			- check against each intents' examples to find a match => detected intent
			- Once you found one, choose randomly one string from the detected intent's responses to speak
			- If the detected intent is 'end', terminate the while loop
			'''

			for intent in intents:
				if SpeechDetection.detectedPhrase in intent["examples"]:
					print(intent)
					if intent['intent'] == "end":
						done = True
					response = random.choice(intent["responses"])
					speak(response)
					break 
			SpeechDetection.detectedPhrase = None
			
	speak("My work is done here. Good bye")

except KeyboardInterrupt:
	print("User keyboard interrupted")
except Exception as e:
	print(e)
finally:
	#print(SpeechDetection.words)
	del SpeechDetection
	myBroker.shutdown()

