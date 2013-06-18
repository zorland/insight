import datetime
import time
import re
import requests
import os

def nws_APICall(zipCode=94305):
	baseStr = 'http://graphical.weather.gov'
	prefix = '/xml/sample_products/browser_interface/ndfdXMLclient.php?zipCodeList='
	suffix = '&product=time-series&pop12=pop12&maxt=maxt&sky=sky&icons=icons'
	zipStr = str(zipCode)
#	print baseStr + prefix + str(zipCode) + suffix
	return baseStr + prefix + str(zipCode) + suffix
#http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?zipCodeList=94305&product=glance

	
#curl -s 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?zipCodeList=94305&product=glance'> out.log
#how does this work in python!!@?!@!


def nws_gatherInfo(apiCall, filename = "default_nws.txt"):
	r = requests.request("GET",apiCall)
	rawData = open(filename,"w")
	rawData.write(r.text)
	rawData.close()
	
	Data = open(filename,"r")
	match = re.findall('<value>([0-9]*)</value>',Data.read())
	return match



def nws_setWeather(forecast = [70,10,0]):

	high = forecast[0]
	cloudy = forecast[1]
	rainy = forecast[2]
	weatherInfo = {}
	print forecast

	if(high > 83):
		weatherInfo['hot'] = True
	if(high < 55 ):
		weatherInfo['cold'] = True
	if(cloudy > 55 ):
		weatherInfo['cloud'] = True
	if(cloudy < 20 ):
		weatherInfo['sun'] = True
	if(rainy > 35 ):
		weatherInfo['rain'] = True
	print weatherInfo	
	return weatherInfo



def nws_getLL(filename = "default_nws.txt"):
	
	if not os.path.isfile(filename):
		return (0,0)
	
	Data = open(filename,"r")
	match = re.search('point latitude="(.*)"\s\w*="(.*)"',Data.read())
	latlng = [float(match.group(1)),float(match.group(2))]
	print latlng
	#    return latlng
	#    print match
	return latlng



def nws_getLocal(fullData, offset =0):
    #formatting highs by day, percip by 12 hour, cloudy by 3 hour
	# high0-7, cloduy 8-48 percip 49-63	
	
	
	cloudyStart = 8 + 8* offset
	rainyStart = 49 + 2* offset
#yuck!
	
	
	high =float(fullData[offset])
	cloudy = (float(fullData[cloudyStart]) + float(fullData[cloudyStart+1]) + float(fullData[cloudyStart+2]))/3
	rainy = (float(fullData[rainyStart]) + float(fullData[rainyStart+1]))/2
	info = [high, cloudy,rainy]
	return info

