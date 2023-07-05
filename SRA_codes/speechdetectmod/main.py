import libpath
import time

import sys
sys.path.append("../lib")
from naoqi import ALModule, ALProxy

class SpeechDetectionModule(ALModule):
	""" 
	A module that handles NAO speech recognition commands based on a vocabulary.
	The vocabulary can be a list of keywords or a list of phrases. Keep the phrases short.
	"""
	
	def exit(self):
		print("exiting module")
		self.memory.unsubscribeToEvent("WordRecognized", self.getName(), "onWordRecognized")
		self.asr.unsubscribe(self.getName())
		ALModule.exit(self)

	def __init__(self, name):
		ALModule.__init__(self, name)
		self.detectedPhrase = None
		self.spottingMode = False
		self.timestamp = time.time()
		self.name = name
		self.memory = ALProxy("ALMemory")
		self.asr = ALProxy("ALSpeechRecognition")
		# need to pause the asr before changing specs
		self.asr.pause(True)
		self.asr.setLanguage("English")
		vocabulary = ["color", "text", "hand", "phone", "stop"]
		self.asr.setVocabulary(vocabulary, self.spottingMode)
		self.asr.pause(False)
		self.asr.subscribe(self.getName())
		self.memory.subscribeToEvent("WordRecognized", self.getName(), "onWordRecognized")


	def onWordRecognized(self, key, value, message):	
		""" A method that handles command recognition. """
		print("Detected speech values:", value)
		
		# check confidences
		# threshold of 0.45 can be fine-tuned
		if(len(value) > 1 and value[1] >= 0.4):
			self.timestamp = time.time()	# record the time
			splits = value[0].split('<...>') #if wordSpotting is enabled, value[0] = "<...> keyword <...>" else "keyword"
			vocab = value[0] if len(splits) == 1 else splits[1].strip()

			# def process_detected_phrase(phrase):
			# 	"""
			# 	A function in the main calling program that handles the detected phrase.
			# 	Modify this function to suit your needs.
			# 	"""
			# 	print("Detected phrase:", phrase)
			# 	if phrase == "color":
            #     # Perform color-related actions
			# 		print("Performing color-related actions")
			# 	elif phrase == "text":
        	# 	# Perform text-related actions
			# 		print("Performing text-related actions")
			# 	elif phrase == "hand":
        	# 	# Perform hand-related actions
			# 		print("Performing hand-related actions")
			# 	elif phrase == "phone":
        	# 	# Perform phone-related actions
			# 		print("Performing phone-related actions")
			# 	elif phrase == "stop":
        	# 	# Perform stop-related actions
			# 		print("Performing stop-related actions")
			# 	else:
        	# 	# Handle unrecognized phrase
			# 		print("Unrecognized phrase:", phrase)		

			'''
			TODO: 
			Add code to capture the detected phrase and pass beyond the handler to the main calling program
			'''
			self.detectedPhrase = vocab
			# if self.detectedPhrase is not None:
			# 	process_detected_phrase(self.detectedPhrase)
			# pass
		else:
			'''
			TODO: 
			Add code here remove the detected phrase and not pass beyond the handler
			'''
			self.detectedPhrase = None
			# pass

	def setVocabulary(self, vocabulary, spotting=False):
		"""Change the vocabulary used"""
		self.asr.pause(True)
		self.spottingMode = spotting
		self.asr.setVocabulary(vocabulary, spotting)
		self.asr.pause(False)

	