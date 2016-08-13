from flask import Flask
from flask import request
from wit import Wit
from fireb import bookReservations

import json
import requests
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def h():
	#return request.args.get('hub.challenge')
	#return 'Starting'	
	#a=json.loads(request.get_json())
	#print a
	a = request.get_json()
	print type(a)
	print ">>>>>>>>>>>>>>>>>>>."
	FBm = a['entry'][0]['messaging']['0']['message']['text']
	return 'asdas'
	'''Wit PUT
	mains(FBm)x`
	'''

@app.route('/receive',methods=['POST','GET'])
def g():
	#return request.args.get('hub.challenge')
	a = request.get_json()
	try:
		mess = a['entry'][0]['messaging'][0]['message']['text']
		#bookReservations()
	except Error:
		print ('Facebook message not obtained')

	return 'hello world'