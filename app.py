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
	#print a
	#print ">>>>>>>>>>>>>>>>>>>"
	try:
		mess = a['entry'][0]['messaging'][0]['message']['text']
		print mess
		userID= a['entry'][0]['messaging'][0]['sender']['id']
		#postFbtext(userID,)
		#witResp(mess)
		getWit(mess)
	except:
		print 'FB message input Failed'

	return 'hello world'

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
	response = {}
	try:
		for key,value in a['entities'].iteritems():
			response[key] = value[0]['value']
			return response
	except:
		print 'Error in removing unwanted fields'