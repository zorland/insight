#searchYelp.py --consumer_key="DywpjGY0b4c5La3lFLSLEQ" --consumer_secret="YwdWOAt1ouQv8f7_B_03dnmQbx0" --token="9pw2FxukYQCYBhUKmOYCLkWBXjhjCAdv" --token_secret="X-i353piFzNyGu2x4eoHD-5ZYkw" --location="511+hamilton+evanston" --term="restaurant"

#"""Command line interface to the Yelp Search API."""
import pandas as pd
import os

def algo_MakePd(weatherInfo = {}, filename = "rest_cache.txt"):

  if not os.path.isfile(filename):
    print "FAILURE"
    return (0,0)
  rests = pd.read_csv(filename, names=['address', 'distance', 'name', 'rating', 'count', 'url', 'id', 'googRate', 'cat', 'priceLevel'])
  #load restaurant info from yelp api call


  #create column for dine-amic score
  rests['dineScore']=1

  # convert to miles
  rests['distance'] *= 0.000622
  

#if google rating is missing default to yelp rating
  for i in range (0,len(rests['dineScore'])):
    if(rests['googRate'][i] == 10):
      rests['googRate'][i] = rests['rating'][i]

  #calculate scores    
  dineScoreRest = algo_CalcJ(rests, weatherInfo)
  return dineScoreRest
                      


def algo_CalcJ(inPd, weatherInfo={}):

  #calculate scores
  restInfo = inPd

  #rain = closest rest
  if('rain' in weatherInfo):
     for i in range (0,len(restInfo['dineScore'])):
       restInfo['dineScore'][i] = 100. - restInfo['distance'][i]*13.
       restInfo['distance'][i] = int(restInfo['distance'][i]*10)/10.0
       #truncate distance
     return restInfo
  

  
  for i in range (0,len(restInfo['dineScore'])):
      scaledRating = algo_scale(restInfo['rating'][i], restInfo['count'][i])
      restInfo['dineScore'][i] *= 50*(scaledRating*2 + restInfo['count'][i]/100. +restInfo['googRate'][i] )
      #apply google and yelp ratings

      if(restInfo['priceLevel'][i] > 3):
        restInfo['dineScore'][i] *= (3/4.)
        #punish for expensive

      restInfo['distance'][i] = int(restInfo['distance'][i]*10)/10.0
      restInfo['dineScore'][i] -= restInfo['distance'][i]*restInfo['distance'][i]/10
      #punish for distance

      if(restInfo['cat'][i]=="Thai" or restInfo['cat'][i]=="Mexican" or restInfo['cat'][i]=="Indian"):
        restInfo['dineScore'][i] *= 2.

  #normalize the dine-amic scores      
  maxNorm =  restInfo.sort("dineScore", ascending= False).values[0][10]
  outPd = restInfo.sort("dineScore", ascending= False)
  for i in range (0,len(outPd['dineScore'])):
       outPd['dineScore'][i] *= 100.
       outPd['dineScore'][i] /= maxNorm

  return outPd
                      


def algo_scale(rating =3, count = 10):
  #account for rests with few reviews and high ratings via wilson confidence interval

  p = rating
  n = count
  z = 3.8
  # square of test statistic for 95 confidence
  if(rating < 2.5):
    return p + (z**2)/(2*n) + (z *((p*(5-p) + z**2/(4*n))/n)**0.5)/(1+z**2/n)
  else:
    return p + (z**2)/(2*n) - (z *((p*(5-p) + z**2/(4*n))/n)**0.5)/(1+z**2/n)
