#searchYelp.py --consumer_key="DywpjGY0b4c5La3lFLSLEQ" --consumer_secret="YwdWOAt1ouQv8f7_B_03dnmQbx0" --token="9pw2FxukYQCYBhUKmOYCLkWBXjhjCAdv" --token_secret="X-i353piFzNyGu2x4eoHD-5ZYkw" --location="511+hamilton+evanston" --term="restaurant"

#"""Command line interface to the Yelp Search API."""
import pandas as pd
import os

def algo_MakePd(weatherInfo = {}, filename = "rest_cache.txt"):

  if not os.path.isfile(filename):
    print "FAILURE"
    return (0,0)
  print "algo success! 1"
  rests = pd.read_csv(filename, names=['address', 'distance', 'name', 'rating', 'count', 'url', 'id', 'googRate', 'cat', 'priceLevel'])
  print rests.ix[0]
  rests['jacq']=1
#  print rests.ix[0]

  rests['distance'] *= 0.000622
  #convert meters to miles

  sortedRest = algo_CalcJ(rests, weatherInfo)

  #pg 128
  print "algo success! 2"
  #rests.sort("rating", ascending= False).values[2]
  return sortedRest
                      


def algo_CalcJ(inPd, weatherInfo={}):
  
  restInfo = inPd
  if('rain' in weatherInfo):
    print "rain"
  if('cloud' in weatherInfo):
    print "cloud"
  if('sun' in weatherInfo):
    print "sun"


  for i in range (0,len(restInfo['jacq'])):
      restInfo['jacq'][i] *= (restInfo['rating'][i]  * restInfo['count'][i] +restInfo['googRate'][i] )
      restInfo['jacq'][i] /= (restInfo['priceLevel'][i])
      restInfo['jacq'][i] -= restInfo['distance'][i]*25
      #need to be clever about ratings and counts.                                                                                                                               
      #I suggest mc study or just throw a mc cone?                                                                                                                               
#      print restInfo['jacq'][i]

  if('hot' in weatherInfo):
    print "hot"
  if('cold' in weatherInfo):
    print "cold"



  return restInfo
                      




