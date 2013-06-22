#test
#searchYelp.py --consumer_key="DywpjGY0b4c5La3lFLSLEQ" --consumer_secret="YwdWOAt1ouQv8f7_B_03dnmQbx0" --token="9pw2FxukYQCYBhUKmOYCLkWBXjhjCAdv" --token_secret="X-i353piFzNyGu2x4eoHD-5ZYkw" --location="511+hamilton+evanston" --term="restaurant"

#"""Command line interface to the Yelp Search API."""
import json
import oauth2
import optparse
import urllib
import urllib2
import os
import re
from googDat import *
import pandas as pd 

def yelp_request(latlng=[44,-90], weatherInfo ={}):
#  cold = True
  print weatherInfo
  url_params ={}
  url_params['ll'] = str(latlng[0])+"," + str(latlng[1])
  #setting up location
  url_params['category'] = "food"
  url_params['limit'] = 20
  #duh
  if("hot" in weatherInfo):
      url_params['term'] = "ice"
  elif("cold" in weatherInfo):
      url_params['term'] = "restaurant+thai+mexican"
  elif("sun" in weatherInfo):
      url_params['term'] = "restaurant+outdoor"
  else:    
    url_params['term'] = "restaurant"



  host = "api.yelp.com"
  path="/v2/search"
  consumer_key = "DywpjGY0b4c5La3lFLSLEQ"
  consumer_secret ="YwdWOAt1ouQv8f7_B_03dnmQbx0"
  token = "9pw2FxukYQCYBhUKmOYCLkWBXjhjCAdv"
  token_secret = "X-i353piFzNyGu2x4eoHD-5ZYkw"

  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
#  print 'URL: %s' % (url,)

  # Sign the URL
  consumer = oauth2.Consumer(consumer_key, consumer_secret)
  oauth_request = oauth2.Request('GET', url, {})
  oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})

  token = oauth2.Token(token, token_secret)
  oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
  signed_url = oauth_request.to_url()
#  print 'Signed URL: %s\n' % (signed_url,)

  # Connect
  try:
    conn = urllib2.urlopen(signed_url, None)
    try:
      response = json.loads(conn.read())
    finally:
      conn.close()
  except urllib2.HTTPError, error:
    response = json.loads(error.read())

  return response


def yelp_findRest(latlng =[44,-90], weatherInfo = {},filename = "yelpOut.txt"):
  response = yelp_request(latlng, weatherInfo)
  rawData = open(filename,"w")
  rawData.write(json.dumps(response, sort_keys=True, indent=2))
#  rawData.write(json.dumps(response), sort_keys=True)
  rawData.close()
  return


def yelp_getRest(latlng =[44,-90],filename = "yelpOut.txt", cacheName = "rest_cache.txt"):

  if not os.path.isfile(filename):
    return (0,0)
  print "Great success!"
  data = open(filename, "r")
  fullText = data.read()
  address = re.findall('display\waddress":\s\[\s*"(.*)"',fullText)
  distance = re.findall('distance":\s(\w*[^.])',fullText)
  name = re.findall('name":\s"([\w\s&\'.-]*[^"])',fullText)
  rating = re.findall('rating":\s(\d.\d)',fullText)
  numRates = re.findall('review_count":\s(\d*)',fullText)
  url = re.findall('mobile_url":\s"(.*[^"])"',fullText)
  ids = re.findall('id":\s"(.*[^"])"',fullText)
  cat = re.findall('categories":\s\[\s*\[\s*"(.*[^"])"',fullText)
  print cat
  numRest = len(ids)

  tupleFile = open(cacheName,"w")
  for x in range(0,numRest-3):
    tupleFile.write(address[x].replace(',', ''))
    tupleFile.write(',')
    tupleFile.write(distance[x])
    tupleFile.write(',')
    tupleFile.write(name[x].replace('\\', ''))
    tupleFile.write(',')
    tupleFile.write(rating[x])
    tupleFile.write(',')
    tupleFile.write(numRates[x])
    tupleFile.write(',')
    tupleFile.write(url[x])
    tupleFile.write(',')
    tupleFile.write(ids[x])
    tupleFile.write(',')

    googData=  goog_APICall(name[x],latlng)
    tupleFile.write(str(googData[0]))
    tupleFile.write(',')
    tupleFile.write(cat[x])
    tupleFile.write(',')
    tupleFile.write(str(googData[1]))

    tupleFile.write('\n')
  tupleFile.close()

  return #match


