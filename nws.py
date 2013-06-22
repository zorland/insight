import datetime
import time
import re
import requests
import os

#CLASS DEF


class Weather:
	'weather class'

	def __init__(self):
		self.weatherImageURL = ""
		self.weatherType = {}
		self.location = []
		self.APICall = ""
		self.forecast = []
		

	def setValues(self, zipCode = 94305):		
		self.setAPICall(zipCode)
		self.setForecast()
		self.setWeather()
		self.setImage()
		self.setLL()
		self.setImage()
		


	def setImage(self):
		url = "/static/images/newsun.png"
		if("rain" in self.weatherType):
			url = "/static/images/rain.png"
		elif("hot" in self.weatherType):
			url = "/static/images/hot.png"
		elif("cold" in self.weatherType):
			url = "/static/images/cold.png"
		elif("cloud" in self.weatherType):
			url = "/static/images/cloud.png"
		self.weatherImageURL = url
			
	def getImage(self):		
		return self.weatherImageURL

	def setLL(self,filename = "default_nws.txt"):
		if not os.path.isfile(filename):
			return (0,0)
	
		Data = open(filename,"r")
		locationInfo = re.search('point latitude="(.*)"\s\w*="(.*)"',Data.read())
		latlng = [float(locationInfo.group(1)),float(locationInfo.group(2))]
		self.location= latlng

	
	def getLL(self):		
		return self.location


	def setWeather(self):
		high = self.forecast[0]
		cloudy = self.forecast[1]
		rainy = self.forecast[2]
		if(high > 83):
			self.weatherType['hot'] = True
		if(high < 55 ):
			self.weatherType['cold'] = True
		if(cloudy > 45 ):
			self.weatherType['cloud'] = True
		if(cloudy < 20 ):
			self.weatherType['sun'] = True
		if(rainy > 35 ):
			self.weatherType['rain'] = True


	def getWeather(self):
		return self.weatherType

	def getForecast(self):
		return self.forecast

	
	def setAPICall(self, zipCode=94305):
		baseStr = 'http://graphical.weather.gov'
		prefix = '/xml/sample_products/browser_interface/ndfdXMLclient.php?zipCodeList='
		suffix = '&product=time-series&pop12=pop12&maxt=maxt&sky=sky&icons=icons'
		zipStr = str(zipCode)
		self.APICall = baseStr + prefix + str(zipCode) + suffix


	def setForecast(self, dayOffset = 0, filename = "default_nws.txt"):
		r = requests.request("GET",self.APICall)
		rawData = open(filename,"w")
		rawData.write(r.text)
		rawData.close()
		Data = open(filename,"r")
		fullData = re.findall('<value>([0-9]*)</value>',Data.read())
    #formatting highs by day, percip by 12 hour, cloudy by 3 hour                                                                                                                    # high0-7, cloduy 8-48 percip 49-63                                                                                                                                      
		cloudyStart = 8 + 8* dayOffset
		rainyStart = 49 + 2* dayOffset

		high =float(fullData[dayOffset])
		
		#average over the day
		cloudy = (float(fullData[cloudyStart]) + float(fullData[cloudyStart+1]) + float(fullData[cloudyStart+2]))/3
		rainy = (float(fullData[rainyStart]) + float(fullData[rainyStart+1]))/2
		
		cloudy = int(cloudy*100)/100.  #truncate the floats                                                                                                
       		rainy = int(rainy*100)/100.
		self.forecast = [high, cloudy,rainy]
	
		
