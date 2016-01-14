# -*- coding: utf-8 -*-
import vk, os, sys, codecs
import urllib.request
import json
import time
import datetime
from random import randint

class VSession (vk.Session, logFile = None)::
	def get_captcha_key(self, captcha_image_url):
		if ( logFile ):
			logFile.write("Captcha is required : " + captcha_image_url)
		response = input("VSession get_captcha_key : Captcha is required, url : " + captcha_image_url)
		return response

class Trollabot(object):
	#File names
	settingsFileName = "settings.json"
	#lists
	settings = ''
	#dictionaries
	emptyMsg = ''
	admins = ''
	#api
	vkApi = None
	#strings
	accessToken = ""
	sorryString = ""
	docsString = ""
	logFileName = ""
	#bools
	printLogs = True
	logToFile = False
	autoStart = True
	#numbers
	newMsg = 0
	waitPeriod = 5.0
	#files
	logFile = None
	#Administrative stuff
	stop = False
	restart = False

	def __init__ (self, settingsFileName = "settings.json", restart = False):
		self.settingsFileName = settingsFileName
		#Trying to open and read the settings file with json
		try:
			with open(settingsFileName) as settingsFile:
				try:
					self.settings = json.load(settingsFile)
				except (NameError):
					self._errorExit("__init__ : JSON NameError - couldn't read setting file with json, please make sure that formatting is correct. For more info, go to json.org")
				except (ValueError):
					self._errorExit("__init__ : JSON ValueError - couldn't read setting file with json, please make sure that formatting is correct. For more info, go to json.org")
		except (IOError,FileNotFoundError):
			self._errorExit("__init__ : settings file not found error. Make sure that it exists and that the path to it is correct.")

		#Settings should contain an array with 2 enrties - "Settings" themselves at settings[0] and "Answers" at settings[1]
		if ( len(self.settings) < 2 ):
			self._errorExit("__init__ : Problem with setting file : incorrect structure. Settings should contain an array with 2 enrties - \"Settings\" themselves at settings[0] and \"Answers\" at settings[1]")

		#
		#Trying to read needed vars from the settings list
		#

		#Trying to read silentMode from settings
		silentMode = self.settings[0].get("silentMode")
		if ( not silentMode ):
			self._errorExit("__init__ : Problem with getting silentMode from settings.json, make sure that such entry exists")
		#Transforming silentMode to a boolean variable (using ternary operators)
		self.printLogs = False if (silentMode == "True") else True
		
		if ( self.printLogs ):
			#Trying to read logToFile from settings
			logToFile  = self.settings[0].get("logToFile")
			if ( not logToFile ):
				self._errorExit("__init__ : Problem with getting logToFile from settings.json, make sure that such entry exists")
			#Transforming logToFile to a boolean variable (using ternary operators)
			self.logToFile = True if (logToFile == "True") else False
			
			#Trying to read docsString from settings
			self.logFileName = self.settings[0].get("logFileName")
			if ( not self.logFileName ):
				self._errorExit("__init__ : Problem with getting logFileName from settings.json, make sure that such entry exists")
			
			#Trying to open logFile
			self.logFile = open(self.logFileName, "w+")
			if ( not self.logFile ):
				self._errorExit("__init__ : Couldn't open logFile")


		#Trying to read accessToken from settings (It is generated automatically by vk.com api, you can get it, using the instructions here https://vk.com/dev/auth_mobile )
		self.accessToken = self.settings[0].get("accessToken")
		if ( not self.accessToken ):
			self._errorExit("__init__ : Problem with getting accessToken from settings.json, make sure that such entry exists")
		
		#Trying to read sorryString from settings
		self.sorryString = self.settings[0].get("sorryString")
		if ( not self.sorryString ):
			self._errorExit("__init__ : Problem with getting sorryString from settings.json, make sure that such entry exists")
		
		#Trying to read docsString from settings
		self.docsString = self.settings[0].get("docsString")
		if ( not self.docsString ):
			self._errorExit("__init__ : Problem with getting docsString from settings.json, make sure that such entry exists")

		#Trying to read admins from settings
		self.admins = self.settings[0].get("admins")
		if ( not self.admins ):
			self._errorExit("__init__ : Problem with getting admins from settings.json, make sure that such entry exists")

		#Trying to read emptyMessage ftom settings (needed in the comparer later to start a loop. This should be just a placeholder message with some values. Example is here : from https://vk.com/dev/messages.get)
		if ( not restart ):
			self.emptyMsg = self.settings[0].get("emptyMsg")
			if ( not self.emptyMsg ):
				self._errorExit("__init__ : Problem with getting emptyMsg from settings.json, make sure that such entry exists")

		"""
		#Trying to decode the emptyMsg using json
		try:
			self.emptyMsg = json.load(emptyMsg)
		except  (NameError):
			self._errorExit("_init__ : JSON NameError - Problem with getting emptyMsg from settings.json, make sure that such entry exists")
		except  (ValueError):
			self._errorExit("__init__ : JSON ValueError - Problem with getting emptyMsg from settings.json, make sure that such entry exists")
		"""
		#Trying to read waitPeriod from settings
		self.waitPeriod = self.settings[0].get("waitPeriod")
		if ( not self.waitPeriod):
			self._errorExit("__init__ : Problem with getting waitPeriod from settings.json, make sure that such entry exists")
	
		#Trying to read autoStart from settings
		self.autoStart = self.settings[0].get("autoStart")
		if ( not self.autoStart ):
			self._errorExit("__init__ : Problem with getting autoStart from settings.json, make sure that such entry exists")
			
		#Transforming autoStart to a boolean variable (using ternary operators)
		self.autoStart = True if (self.autoStart == "True") else False

		#
		#Ended reading the variables from settings
		#

		if ( self.printLogs ):				
			logStart = "__init__ : starting trollabot, "
			logStart += "\nSettings  :  \n" + str(json.dumps(self.settings[0], indent = 4, sort_keys = False))
			logStart +=  "\nAnswers : \n" + str(json.dumps(self.settings[1], indent = 4, sort_keys = True, ensure_ascii = False))	
			self._log(logStart)
			session = VSession(access_token = self.accessToken, logFile = self.logFile)
		else:
			session = VSession(access_token = self.accessToken)
		self.vkApi = vk.API(session)
		if ( self.autoStart or restart ):
			self.start()

	def start(self):
		oldMsg = self.emptyMsg
		while ( not self.restart ):
			oldMsg = self._getMsg(oldMsg = oldMsg)
			time.sleep(self.waitPeriod)
		#Restart is true at this point, so restart:
		self.restart = False
		self.emptyMsg = oldMsg
		self.restartSelf()

	def restartSelf(self):
		self.__init__(settingsFileName = self.settingsFileName, restart = True)

	def _getMsg ( self, oldMsg="" ):
		newMsg = self.vkApi.messages.get(count = 1) #get the newest message
		if ( self.printLogs ):
			self._log("_getMsg : Getting a message..")
			self._log("_getMsg : OldMsg date, body  = " + str(oldMsg[1].get('date')) + "," + str(oldMsg[1].get('body')))
			self._log("_getMsg : NewMsg date, body = " + str(newMsg[1].get('date')) + "," + str(newMsg[1].get('body')))
		if (  newMsg[1].get('body') != oldMsg[1].get('body') and
		      newMsg[1].get('date') != oldMsg[1].get('date')): #if it's new, parse it
			dialogue = False
			#self._log(newMsg)
			sendID = newMsg[1].get('chat_id')
			#self._log(newMsg[1])
			if ( sendID == None ):
				#chatID is empty, so it's a dialogue.
				dialogue = True
				sendID = newMsg[1].get('uid')
			msgBody = newMsg[1].get('body').lower().replace(u'\u0456', u'i')
			if ( self.printLogs ):
				self._log("_getMsg : Sending a message to a parser : sendID = " + str(sendID) + ", dialogue mode = " + str(dialogue) + " ,Message = \"" + str(msgBody.encode('utf-8')) +"\"")
			self._parseMsg( sendID = sendID, msg = msgBody, dialogue = dialogue )
		return newMsg

	def  _parseMsg( self, sendID = 1, msg = '', dialogue = False ):
		sendSorry = False
		originalMsg = msg
		msg = msg.split('\n')[0].lower()
		msg = msg.split('!') #If it starts with !, then it's a command and we should parse it
		response = None
		if ( len(msg) > 1 ):
			msg = msg[1].split(' ') 
			if ( len(msg) > 1 ):
				if ( self.printLogs ):
					self._log("_parseMsg : Message length is > 2, parsing it using if statements")
					self._log("_parseMsg : Parsing message : \"" + str(msg) + "\"")
				if ( msg[0] == 'roll'):
					if ( len(msg) > 1 ):
						msg = msg[1].split('d')
						if ( len(msg) > 1 ):
							try:
								response = "Rolling a d" + str(msg[1]) + "...\n" + str(randint(1,int(msg[1]))) + "!"
							except ValueError:
								if ( self.printLogs ):
									self._log("_parseMsg : ValueError exception while trying to roll a die. setting response = None")
								response = None
						else:
							if ( self.printLogs ):
								self._log("_parseMsg : Couldn't find a number to roll (ex. command = \"!roll d\" instead of \"!roll d6\")" )
							response = None
					else:
						response = 'No die specified. For example, try using \"!roll d6\", \"!roll d20\", etc. :)'
				else:
					sendSorry = True
					response = None
			else :
				msg = msg[0] #transform msg into a string from a list
				if ( self.printLogs ):
					self._log("_parseMsg : Message length is < 2, parsing it using dictionaries")
					self._log("_parseMsg : Message after removing \"!\" : " + str(msg))
				response = self.settings[1].get(msg)
				if ( not response ):
					sendSorry = True
					if ( sendID in self.admins.values() ):
						if ( self.printLogs ):
							self._log("_parseMsg : Parsing an admin command " + str(originalMsg))
						if ( msg == "restart" ):
							self.restart = True
							response = "Restarting trollabot"
						elif ( msg == "stop"):
							response = "Stopping trollabot"
							response = self._sendMsg(sendID = sendID, msg = response, dialogue = dialogue)
							self.stop = True
							return response;
						elif ( msg == "start"):
							if ( self.stop ):
								response = "Starting trollabot"
								self.stop = False
							else: 
								response = "Trollabot has already started"
						elif ( msg == "exit"):
							response = "Exiting trollabot. You'll have to manually re-enable me on the server to work again."
							self._sendMsg(sendID = sendID, msg = response, dialogue = dialogue)
							self._exit("Exit command gotten from an admin")
		else:
			if ( self.printLogs ):
				self._log("_parseMsg : Message isn't a command")
		if (response):
			if ( self.printLogs ):
				self._log("_parseMsg : Sending a response " + str(response) + " to _sendMsg" )
			return self._sendMsg(sendID = sendID, msg = response, dialogue = dialogue)
		else:
			if ( self.printLogs ):
				self._log("_parseMsg : Couldn't parse the message \"" + str(originalMsg) + "\",  sendSorry = " + str(sendSorry) )
			if ( sendSorry ):
				return self._sendSorry(sendID = sendID, originalMsg = originalMsg, dialogue = dialogue)


	def _incRequest ( self, message = ''):
		response = None
		if ( message ):
			if ( self.printLogs ):
				self._log( "_incRequest : generating an incorrect request message")
			response = self.sorryString + message + '\n' + 'Docs : ' + self.docsString
		else :
			if ( self.printLogs ):
				self._log( "_incRequest : Couldn't genarate an incorrect request message : Original message is null")
		return response

	def _sendSorry ( self, sendID = 1, originalMsg = '', dialogue = False):
		if ( originalMsg ):
			response = self._incRequest(message = originalMsg)
			if ( self.printLogs ):
				self._log("_sendSorry : Senging a sorry response to " + str(sendID) + ", dialogue = " + str(dialogue))
		else:
			if ( self.printLogs ):
				self._log("_sendSorry : Couldn't generate a sorry message : original message is null")
		self._sendMsg(dialogue = dialogue, sendID = sendID, msg = response)

	def _sendMsg( self, sendID ="", msg="TestMessage", dialogue = False ):
		if ( not self.stop ):
			if ( msg ):
				if ( dialogue ):
					if ( self.printLogs ):
						self._log("_sendMsg : Sending a message to a user : sendID = " + str(sendID) +  ", Message = \"" + msg + "\"" )
					response = self.vkApi.messages.send(uid = sendID, message = msg)
				else:
					if ( self.printLogs ):
						self._log("_sendMsg : Sending a message to a chat : sendID = " + str(sendID) +  ", Message = \"" + msg + "\"" )
					response = self.vkApi.messages.send(chat_id = sendID, message = msg)
			else :
				response = "Couldn't print a message : message is null"
		else:
			response = "Not sending a message because !stop command is in effect"
		if ( self.printLogs ):
			self._log("_sendMsg : Vk api response : " + str(response))
		return response

	def _errorExit (self, msg = "Unknown error"):
		errorMsg = "trollabot " + msg
		if ( self.printLogs ):
			self._log(errorMsg)
		self._exit(errorMsg)

	def _exit (self, msg = ""):
		sys.exit(msg)

	def _log (self, msg = ""):
		response = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  " - trollabot " + msg + "\n"
		if ( self.logToFile ):
			self.logFile.write(response)
		else:
			print(response)

def main():
	bot = Trollabot()

if __name__ == "__main__":
	main()

