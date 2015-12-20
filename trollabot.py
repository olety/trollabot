# -*- coding: utf-8 -*-
import vk, os, json, sys, codecs
from random import randint

class Trollabot(object):
	vkApi = None
	token = ""
	newMsg = 0

	def __init__ (self, accessToken, autoStart = False):
		print("Starting trollabot, access token =  " + accessToken)
		self.token = accessToken
		session = vk.Session(access_token = self.token)
		self.vkApi = vk.API(session)
		if ( autoStart ):
			self.startParsing()
	
	def startParsing(self):
		oldMsg = self.vkApi.messages.get(count = 1) 
		#while ( 1 ):
		#	oldMsg = self._getMessage(oldMsg = oldMsg)
		oldMsg = self._getMessage(oldMsg = oldMsg)

	def _getMessage ( self, oldMsg="" ):
		newMsg = self.vkApi.messages.get(count = 1) #get the newest message
		if ( newMsg[1].get('uid') == oldMsg[1].get('uid') and 
                     newMsg[1].get('body') == oldMsg[1].get('body') and
		      newMsg[1].get('date') == oldMsg[1].get('date')): #if it's new, parse it
			dialogue = False
			sendID = newMsg[1].get('chat_id')
			#print(newMsg[1])
			if ( sendID == None ):
				#chatID is empty, so it's a dialogue.
				dialogue = True
				sendID = newMsg[1].get('uid')
			msgBody = newMsg[1].get('body')
			print("Sending a message to a parser : sendID = " + str(sendID) + " , msgBody = " + msgBody + ", dialogue mode = " + str(dialogue))
			self._parseMessage( sendID = sendID, msg = msgBody, dialogue = dialogue ) 
			
		return newMsg	
	
	def  _parseMessage ( self, sendID = 1, msg = "", dialogue = False ):
		msg = msg.lower()
		msg = msg.replace(u'\u0456', u'i')
		msg = msg.split("!",1) #If it starts with !, then it's a command and we should parse it
		if ( len(msg) > 1 ):
			msg = msg[1].split(" ")
			if ( msg[0] == "roll"):
				if ( len(msg) > 1 ):	
					if ( msg[1] == "d6" ):
						self._printMsg(dialogue = dialogue, sendID = sendID, msg = "Rolling a d6.. " + str(randint(1,6)) + "!")
				else:
					self._printMsg(dialogue = dialogue, sendID = sendID, msg = "No die specified, rolling a d6.. " + str(randint(1,6)) + "!")
				
		else:
			print("Message isn't a command")

	def _printMsg( self, sendID ="", msg="TestMessage", dialogue = False ):
		if ( dialogue ):
			print("Sending message: " + str(msg) + " , To user_id = " + str(sendID))
			#response = self.vkApi.messages.send(user_id = sendID, message = "trollabot test")
		else:
			print("Sending message: " + str(msg) + " , To chat_id = " + str(sendID))
			#response = self.vkApi.messages.send(chat_id = chatID, message = "trollabot test")

def main():
	'''
	loginInfo structure :
	access token
 	appID
 	email
 	pasw
	'''
	fileName = "loginInfo.txt"
	loginInfo = open(fileName, "r")
	token = (loginInfo.readline()).split("\n")[0]
	# token = "123123\n", and we have to pass only "123123", so we split it by \n and use the first part
	bot = Trollabot(accessToken = token, autoStart = True)
	


if __name__=="__main__":
	main()
