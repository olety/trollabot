# -*- coding: utf-8 -*-
import vk, os, sys, codecs
import daemon
import urllib.request
import json
import time
from random import randint

class VSession (vk.Session):
	def get_captcha_key(self, captcha_image_url):
		response = input("Captcha is required, url : " + captcha_image_url)
		return response

class Trollabot(object):
	vkApi = None
	token = ""
	newMsg = 0
	waitPeriod = 5.0
	emptyMsg = """
			[63,
			 {
				"read_state": 1, 
				"title": " ... ", 
				"mid": 89, 
				"out": 0, 
				"date": 1451081626,
				"body": "asdtest", 
				"uid": 777
			}]
		   """

	def __init__ (self, accessToken, autoStart = False, waitPeriod = 5.0):
		print("Starting trollabot, access token =  " + accessToken)
		self.waitPeriod = waitPeriod
		self.token = accessToken
		session = VSession(access_token = self.token)
		self.vkApi = vk.API(session)
		if ( autoStart ):
			self.start()
	
	def start(self):
		oldMsg = json.loads(self.emptyMsg)
		while ( 1 ):
			oldMsg = self._getMsg(oldMsg = oldMsg)
			time.sleep(self.waitPeriod)
		#oldMsg = self._getMsg(oldMsg = "")

	def _getMsg ( self, oldMsg="" ):
		newMsg = self.vkApi.messages.get(count = 1) #get the newest message
		print ( "Getting a message..")
		print ( "OldMsg date, body  = " + str(oldMsg[1].get('date')) + "," + str(oldMsg[1].get('body')))
		print ( "NewMsg date, body = " + str(newMsg[1].get('date')) + "," + str(newMsg[1].get('body')))
		if (  newMsg[1].get('body') != oldMsg[1].get('body') and
		      newMsg[1].get('date') != oldMsg[1].get('date')): #if it's new, parse it
			dialogue = False
			print(newMsg)
			sendID = newMsg[1].get('chat_id')
			#print(newMsg[1])
			if ( sendID == None ):
				#chatID is empty, so it's a dialogue.
				dialogue = True
				sendID = newMsg[1].get('uid')
			msgBody = newMsg[1].get('body').lower().replace(u'\u0456', u'i')
			print("Sending a message to a parser : sendID = " + str(sendID) + ", dialogue mode = " + str(dialogue) + " ,Message =")
			sys.stdout.buffer.write(msgBody.encode('utf-8'))
			print()		
			self._parseMsg( sendID = sendID, msg = msgBody, dialogue = dialogue ) 	
		return newMsg	
	
	def  _parseMsg( self, sendID = 1, msg = "", dialogue = False ):
		msg = msg.split("!",1) #If it starts with !, then it's a command and we should parse it
		if ( len(msg) > 1 ):
			msg = msg[1].split(" ")
			if ( msg[0] == "roll"):
				if ( len(msg) > 1 ):	
					if ( msg[1] == "d6" ):
						self._printMsg(dialogue = dialogue, sendID = sendID, msg = ("Rolling a d6.. " + str(randint(1,6)) + "!"))
				else:
						self._printMsg(dialogue = dialogue, sendID = sendID, msg = ("No die specified, rolling a d6.. " + str(randint(1,6)) + "!"))
				
		else:
			print("Message isn't a command")

	def _printMsg( self, sendID ="", msg="TestMessage", dialogue = False ):
		print("1")
		if ( dialogue ):
			print("Sending a message to a user : sendID = " + str(sendID) +  " ,Message =")
			sys.stdout.buffer.write(msg.encode('utf-8'))
			print()				
			response = self.vkApi.messages.send(uid = sendID, message = msg)
		else:
			print("Sending a message to a chat : sendID = " + str(sendID) +  " ,Message =")
			sys.stdout.buffer.write(msg.encode('utf-8'))
			print()				
			response = self.vkApi.messages.send(chat_id = sendID, message = msg)
		return response

def main():
	#daemon stuff 
	pid = str(os.getpid())
	pidfile = "/tmp/mydaemon.pid"
	if os.path.isfile(pidfile):
   		 print ('%s already exists, exiting' % pidfile)
   		 sys.exit()
	else:
   		 open(pidfile, 'w').write(pid)
	'''
	loginInfo structure :
	authToken
	appID
	appSecret
 	email
 	password
	loginType
	loginScope
	'''
	loginFileName = "loginInfo.txt"
	settingsFileName = "Settings.txt"
	loginInfo = []
	settings = []
	with open(loginFileName) as loginInfoFile:
		for line in loginInfoFile:
			loginInfo.append(line.split("\n")[0])

	with open(settingsFileName) as settingsFile:
		for line in settingsFile:
			settings.append(line.split("\n")[0])
	# appID = "123123\n", and we have to pass only "123123", so we split it by \n and use the first part
	#acces token is generated by the vk.com and returned via json
	print(loginInfo)
	print(settings)
	token = loginInfo[0]
	bot = Trollabot(accessToken = token, autoStart = True, waitPeriod = float(settings[0]))
	os.unlink(pidfile)
	


#if __name__=="__main__":
with daemon.DaemonContext():
	main()
