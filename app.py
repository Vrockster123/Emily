from flask import Flask
from flask import request
from wit import Wit
import json
import requests
import os
import time as tim
app = Flask(__name__)
followup = 0

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
		if followup == True:
			followup = False
			return	
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
    timeA = dicteg.get('datetime',"")
    seatno = dicteg.get('number_seats' ,"")
    fooditems = dicteg.get('fooditems',"")

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
                print 'selected Book'
            elif value == "order" or value == "preorder": 	
                mode = 2  
            elif value == "specials": 
                mode = 3
            else:
            	mode = 0
    if mode == 1: 
        aa=reservation(location,timeA,seatno,userId)
        return aa
    if mode == 2: 
    	print 'outside for loop',mode
        bb= preorder(location,fooditems,userId)
        return bb
    if mode == 3:
    	cc= getSpecials(location,userId)
    	return cc
    else:
    	postFbtext(userId,"Sorry! I didnt quite understand what you said, but I get better with time like old wine!")
    	return "Sorry! I didnt quite understand what you said, but I get better with time like old wine!"
    print 'Ending function'

def firebaseJSON():
	try:
		string = "curl https://emily-c3113.firebaseio.com/.json > temp3.txt"
		os.system(string)
	except:
		print 'Error while accessing firebase'
	with open("temp3.txt", "r") as ins:
			a = json.load(ins)
	return a


def reservation(location,timeA,seatno,userID):
	'''if location == "":
		followup = True'''
	print '>>>>>>>>>>>>>>>>Done'
	a=firebaseJSON()
	#print a
	#dic = {"behaviorMode":1,"seatsRequired":seatno,"wait":"1"}
	a['behaviorMode']="1"	
	string = "curl -X PUT -d '" + json.dumps(a) +" 'https://emily-c3113.firebaseio.com/.json'"
	#print ">>>>>>" + string
	os.system(string) 
	a['wait']="1"
	string = "curl -X PUT -d '" + json.dumps(a) +"' 'https://emily-c3113.firebaseio.com/.json'"
	os.system(string) 
	a['seatsRequired']=str(seatno)
	string = "curl -X PUT -d '" + json.dumps(a) +"' 'https://emily-c3113.firebaseio.com/.json'"
	os.system(string) 
	#print "asdas" +  string	
	while True:
		tim.sleep(3)
		'''os.system("curl https://emily-c3113.firebaseio.com/wait.json > temp3.txt")
		with open("temp3.txt", "r") as ins:
				b = json.load(ins)
		#print type(b),b
		if(str(b) == "0"):'''
		break
	#print 'outside'
	os.system("curl https://emily-c3113.firebaseio.com/response.json > temp3.txt")
	with open("temp3.txt", "r") as ins:
		b = json.load(ins)
	print b

	if str(b) == "yes":
		postFbtext(userID,"Yes. The table for " + seatno + " was available at " + location +" and the booking was confirmed for " + timeA )
		return str("Yes. The table for " + seatno + " was available at " + location +" and the booking was confirmed for " + timeA)
	else:
		postFbtext(userID,"No. Sorry, the table for " + seatno +" was not available at" +location + " on " + timeA )
		return str("No. Sorry, the table for " + seatno +" was not available at" +location + " on " + timeA)


def preorder(location,fooditems,userID):
	print 'here >>>>>'
	try:
		a=firebaseJSON()
		#print a
		#dic = {"behaviorMode":1,"seatsRequired":seatno,"wait":"1"}
		a['behaviorMode']="2"
		string = "curl -X PUT -d '" + json.dumps(a) +" 'https://emily-c3113.firebaseio.com/.json'"
		#print ">>>>>>" + string
		os.system(string) 
		a['order']=str(fooditems)
		string = "curl -X PUT -d '" + json.dumps(a) +"' 'https://emily-c3113.firebaseio.com/.json'"
		os.system(string)
		a['wait']="1"
		string = "curl -X PUT -d '" + json.dumps(a) +"' 'https://emily-c3113.firebaseio.com/.json'"
		os.system(string) 
		#print "asdas" +  string	
		while True:
			tim.sleep(3.5)
			'''os.system("curl https://emily-c3113.firebaseio.com/wait.json > temp3.txt")
			with open("temp3.txt", "r") as ins:
					b = json.load(ins)
			print type(b),b
			if(str(b) == "0"):'''
			break
		#print 'outside'
		os.system("curl https://emily-c3113.firebaseio.com/response.json > temp3.txt")
		with open("temp3.txt", "r") as ins:
			b = json.load(ins)
		print b
		if str(b) == "yes":
			postFbtext(userID,"Yes. The preorder for "+ fooditems+ " was placed in " + location )
			return str("Yes. The preorder for "+ fooditems+ " was placed in " + location )
		else:	
			postFbtext(userID,"Sorry, "+location +" failed to accept order of " + fooditems )
			return str("Sorry, "+location +" failed to accept order of " + fooditems )
	except:
		print 'Error in order'

from query import Specials,getQuery
def getSpecials(location,userID):
	try:
		a=getQuery()
		A =Specials(a,location)
		string= ""
		if len(A) == 0:
			string = "Currently " + location + " does not have a chef suggested specials"
		else:
			string =location + " is known for"
		for i in A:
			string = string + str(i) + ", "
		postFbtext(userID,string)
		return string
	except:
		print 'Error in Specials'


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
