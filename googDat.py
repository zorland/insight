import datetime
import time
import re
import requests
import os
import json
import urllib

def goog_APICall(restName ="blue&fish", latlng="-33.867,151.2"):

	locString = str(latlng[0])+"," + str(latlng[1])
	restName = restName.replace('&', '')
	callName = re.sub(r"\s+", '&', restName)
#	callName = restName.replace(' ', '&')
	print callName
	baseStr = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
	middleStr = '&radius=3000&types=food&name='
	suffix = '&sensor=false&key=AIzaSyBRAegE--xWfdAJQCkehT6j1y0Ic_KOBik'
#	print "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&types=food&name=fish&sensor=false&key=AIzaSyBRAegE--xWfdAJQCkehT6j1y0Ic_KOBik"	
	print baseStr + locString+ middleStr+  callName +suffix
	apiCall = baseStr + locString+ middleStr+  callName +suffix

#	filename = "default_goog.txt"
#	r = requests.request("GET",apiCall)
#	rawData = open(filename,"w")
#	rawData.write(r.text)
#	rawData.close()

	googleResponse = urllib.urlopen(apiCall);
	jsonResponse = json.loads(googleResponse.read())
	s= jsonResponse['results']
	priceLev = 2 # this is a sad default but cant do better
	stars = 10
	print "LENGTH =" + str(len(s))
	if (len(s) > 0):
		if('price_level' in s[0]):
			priceLev = s[0]['price_level']
		if('rating' in s[0]):
			stars = s[0]['rating']
			print s[0]['rating']
		return (stars, priceLev)			
	return (10,10)




 
def goog_City(zipCode = 94305):

	apiCall = "http://maps.googleapis.com/maps/api/geocode/json?address="
	apiCall += str(zipCode)
	apiCall += "&sensor=false"
	try:
		googleResponse = urllib.urlopen(apiCall)
		jsonResponse = json.loads(googleResponse.read())
		s= jsonResponse['results']
		d = s[0]['address_components']
		name = d[1]['long_name']
		print name
		return name
	except:
		return zipCode
