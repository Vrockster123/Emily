import requests
import ssl
import os
import json
Query_URL = "http://data.assured53.hasura-app.io/v1/query"
def getQuery():

	string ="curl -X POST -H \"Authorization: Bearer 98y006e79b8oo9cm8purddy3b4eip4ls\" -H \"Content-Type: application/json\" -H \"Cache-Control: no-cache\" -H \"Postman-Token: 4bd77c73-8de1-b357-1a4c-d9b55615e37f\" -d '{ \
    \"type\": \"select\", \
    \"args\": {\
        \"table\": \"hotel\",\
        \"columns\": [\"*\", {\"name\": \"items\", \"columns\": [\"*\"]}]\
    }\
}       ' \"https://data.assured53.hasura-app.io/v1/query\""
	os.system(string + "> temp2.txt")
	try:
		with open("temp2.txt", "r") as ins:
			a = json.load(ins)
		for x in a:
			print x['name']
		return a
	except:
		print 'Error in converting txt file to Json'


#returns restaurants that are in cuisine[]
def SpecialCheck(a,cuisine):
	rests = []
	for i in a:
		for j in i['items']:
			if j['cuisine'] in cuisine and j['speciality'] == True:
				rests.append(i['name'])
			break
	return rests

#returns restaurants that have Special dishes, bot should ask for booking a reservation
def SpecialDish(a,dish):
	rests = []
	for i in a:	
		for j in dish:
			if j.lower() not in [x['name'].lower() for x in i['items']]:
				break
			rests.append(i['name'])
	a = []
	for x in set(rests):
		if(rests.count(x) == len(dish)):
			a.append(x)
	return a


#Man:- Is there is atleast 1  <dish> present in <rest>
def isAvail(rest,dish):
	rests = []
	for i in a:
		for j in i['items']:
			if j['name'].lower() in dish.lower():
				rests.append(i['name'])
				break
	return rests

def Specials(a,rest):
	specials = []
	for i in a:
		if i['name'].lower() == rest.lower():
			for j in i['items']:
				if j['speciality'] == True:
					specials.append(j['name'])
	return specials

def CalcCost(a,rest,dishes):
	cost = 0
	for i in a:
		if i['name'] == rest :
			for j in i['items']:
				if j['name'] in dishes:
					cost = cost + j['price']

	return cost