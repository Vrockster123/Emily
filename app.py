from flask import Flask
from flask import request
from wit import Wit
import json
import requests
import os
app = Flask(__name__)

@app.route('/receive',methods=['POST','GET'])

def g():
	#return request.args.get('hub.challenge')
	a = request.get_json()
	print a
	#print ">>>>>>>>>>>>>>>>>>>"
	try:
		mess = a['entry'][0]['messaging'][0]['message']['text']
		print mess
		userID= a['entry'][0]['messaging'][0]['sender']['id']
		#postFbtext(userID,)
		#witResp(mess)
		#getWit(mess)
	except:
		print 'FB message input Failed'
	try:
		print (respond(userID, mess))
	except:
			print 'Error in response'

	return 'hello world'

def respond(userId,message): 
    #print('Hello World!')
    dicteg = getWit(message)
    print dicteg
    mode = 0;
    location = dicteg.get('location' ,"")
    time = dicteg.get('datetime',"")
    seatno = dicteg.get('number_seats' ,"")

    for key,value in dicteg.iteritems():                     
        if key == "self_enquiry":
        	postFbtext(userId,'My name is Emily and I was designed by Varun and Roopesh, at SSN.Also, I promise not to destroy humanity :)')
        	return 'My name is Emily and I was designed by Varun and Roopesh, at SSN.Also, I promise not to destroy humanity :)'
        elif key == "greeting":
        	postFbtext(userId,'Hello there!')
        	return 'Hello there!'
        elif key == "action":
            if value == "book": 
                mode = 1
            if value == "order" or value == "preorder": 
                mode = 2  
            if value == "specials": 
                mode = 3
    if mode == 1: 
        return location+" "+time+" "+seatno
    if mode == 2: 
        return location+" "+order
    if mode == 3:
    	return location

Witaccess_token = "LVLKPQNZ5IEMVZ6OB5QHGSUZGBBGZCNM"	

def witResp(message):
	try:
		client = Wit(access_token=Witaccess_token)
		resp = client.message(message)
	except:
		print 'Error in wit message() API'

def getJson(userID):
	a={
	  "recipient":{
	    "id": str(userID)
	  },
	  'message':{
	    "text":"hello, world!"
	  }
	}
	return a

def fileToJson(txtfile):
	try:
		with open(txtfile, "r") as ins:
			a = json.load(ins)
	   	return a
	except:
		print 'Error in converting txt file to Json'

def postFbtext(userID,msg):
	#print string
	try:
		string ="curl -X POST -H \"Content-Type: application/json\" -d \'{ \
	  \"recipient\":{	\
	    \"id\":\"" + str(userID) + "\" \
	  },	\
	  \"message\":{ \
	    \"text\":\"" + str(msg) +"\" \
	  } \
	}' \"https://graph.facebook.com/v2.6/me/messages?access_token=EAAD5596IWWYBABpdG4yEChjuvAqU2HQ0xZBYDo48BXrXPBTvcU6yUeXplDdPA63YVGPl7eIBr2AH2sfDwaouq6mkrpNn1VVueP0pHin9s81S2wQtJvveZA3G6fr7NXBKtKHUlLFX2PMzlT5Y8K14q39bHRCh6pjGReZA8IKlQZDZD\""
		os.system(string)
	except:
		print 'Error in Posting to FB'



def getWit(mess):
	mess=mess.replace(" ","%20")
	cmd = "curl -H 'Authorization: Bearer LVLKPQNZ5IEMVZ6OB5QHGSUZGBBGZCNM' 'https://api.wit.ai/message?v=20160813&q=" + mess + "'"
	os.system(cmd + " > temp.txt")
	a=fileToJson("temp.txt")
	#print a
	response = {}
	try:
		for key,value in a['entities'].iteritems():
			response[key] = value[0]['value']
		return response
	except:
		print 'Error in removing unwanted fields'
