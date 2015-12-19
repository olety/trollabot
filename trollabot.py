# -*- coding: utf-8 -*-
import vk, os, json, sys, codecs
from random import randint

def main():
	'''
	loginInfo structure :
	key
 	appID
 	email
 	pasw
	'''
	fileName = "loginInfo.txt"
	loginInfo = open(fileName, "r")
	key = (loginInfo.readline()).split("\n")[0]
	# key = "123123\n", and we have to pass only "123123", so we split it by \n and use the first part
	print("Identification key : " + key)
	session = vk.Session(access_token = key)
	vkapi = vk.API(session)
	#response = vkapi.messages.send(chat_id = chatID, message = "trollabot test")
	response =vkapi.messages.get(count = 1)	
	print(response[0])
	print(response[1].get('chat_id'))
	message = response[1].get('body')#.encode('utf-8')
	sys.stdout.buffer.write(message.replace(u'\u0456', u'i').encode('utf-8'))
	sys.stdout.buffer.write('\n'.encode('utf-8'))
	sys.stdout.flush()
	parseMessage(vkApi = vkapi, chatID = 1, msg = "!roll d6")

def getMessage ( vkApi = None, oldMsg="" ):
	newMsg = vkapi.messages.get(count = 1)
	if ( set(newMsg).difference(oldMsg) == set() ):
		return
	else: 
		chatID = response[1]['chat_id']
		msgBody = response[1].get('body')
		parseMessage( vkApi = vkApi, chatID = newMsg, msg = msgBody ) 	
		
	
def  parseMessage ( vkApi = None, chatID = 1, msg = "" ):
	msg.lower()
	msg = msg.split("!",1)
	if ( msg[1] ):
		msg = msg[1].split(" ")
		if ( msg[0] == "roll"):
			if ( msg[1] == "d6" ):
				printMsg(chatID = chatID, msg = randint(1,6))
			
	else:
		print("command is empty")

def printMsg( chatID ="", msg="TestMessage" ):
	print("Sending message : " + str(msg) + " , To chat_id = " + str(chatID))

if __name__=="__main__":
	main()
