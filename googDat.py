import datetime
import time
import re
import requests
import os
import json
import urllib

def goog_APICall(restName ="blue&fish", latlng="-33.867,151.2"):

	#API call based on zipcode lat/long
	locString = str(latlng[0])+"," + str(latlng[1])
	restName = restName.replace('&', '')
	callName = re.sub(r"\s+", '&', restName)
	baseStr = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
	middleStr = '&radius=3000&types=food&name='
	suffix = '&sensor=false&key=AIzaSyBRAegE--xWfdAJQCkehT6j1y0Ic_KOBik'
	apiCall = baseStr + locString+ middleStr+  callName +suffix

	#get JSON file from API call
	googleResponse = urllib.urlopen(apiCall);
	jsonResponse = json.loads(googleResponse.read())
	s= jsonResponse['results']
	priceLev = 2 
	stars = 10 #set default beyond possible values -- if no rating in google, algo.py takes care of it
#	print "LENGTH =" + str(len(s))
	if (len(s) > 0):
		if('price_level' in s[0]):
			priceLev = s[0]['price_level']
		if('rating' in s[0]):
			stars = s[0]['rating']
			print s[0]['rating']
		return (stars, priceLev)			
	return (10,10)




 
def goog_City(zipCode = 94305):

	#find city name from zipcode
	apiCall = "http://maps.googleapis.com/maps/api/geocode/json?address="
	apiCall += str(zipCode)
	apiCall += "&sensor=false"
	try:
		googleResponse = urllib.urlopen(apiCall)
		jsonResponse = json.loads(googleResponse.read())
		s= jsonResponse['results']
		d = s[0]['address_components']
		name = d[1]['long_name']
		return name
	except:
		return zipCode
