from flask import Flask
from flask import request
from wit import Wit
import json
import requests
import os
app = Flask(__name__)

@app.route('/receive',methods=['POST','GET'])
def g():
	a = request.get_json()
	#print a
	#print ">>>>>>>>>>>>>>>>>>>"
	try:
		mess = a['entry'][0]['messaging'][0]['message']['text']
		print mess
		userID= a['entry'][0]['messaging'][0]['sender']['id']
		#postFbtext(userID,)
		#witResp(mess)
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

	
