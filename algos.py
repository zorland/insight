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


  # clean values
  rests['distance'] *= 0.000622

  for i in range (0,len(rests['jacq'])):
    if(rests['googRate'][i] == 10):
      rests['googRate'][i] = rests['rating'][i]
      


  jacqRest = algo_CalcJ(rests, weatherInfo)


  print "algo success! 2"
  #rests.sort("rating", ascending= False).values[2]
  print jacqRest['jacq']
  return jacqRest
                      


def algo_CalcJ(inPd, weatherInfo={}):
  
  restInfo = inPd
  

  if('rain' in weatherInfo):
     for i in range (0,len(restInfo['jacq'])):
       restInfo['jacq'][i] = 100. - restInfo['distance'][i]*13.
       restInfo['distance'][i] = int(restInfo['distance'][i]*10)/10.0
     return restInfo
  

  for i in range (0,len(restInfo['jacq'])):
      scaledRating = algo_scale(restInfo['rating'][i], restInfo['count'][i])
      restInfo['jacq'][i] *= 50*(scaledRating*2 + restInfo['count'][i]/100. +restInfo['googRate'][i] )
      if(restInfo['priceLevel'][i] > 3):
        restInfo['jacq'][i] *= (3/4.)
      restInfo['distance'][i] = int(restInfo['distance'][i]*10)/10.0
      restInfo['jacq'][i] -= restInfo['distance'][i]*restInfo['distance'][i]/10
      if(restInfo['cat'][i]=="Thai" or restInfo['cat'][i]=="Mexican" or restInfo['cat'][i]=="Indian"):
        restInfo['jacq'][i] *= 2.
        
      if(restInfo['cat'][i]=="Ethnic Food"):
        restInfo['jacq'][i] *= 0.
      #stupid hack =(  

  #normalize the dine-amic scores      
  maxNorm =  restInfo.sort("jacq", ascending= False).values[0][10]
  outPd = restInfo.sort("jacq", ascending= False)
  for i in range (0,len(outPd['jacq'])):
       outPd['jacq'][i] *= 100.
       outPd['jacq'][i] /= maxNorm

  return outPd
                      


def algo_scale(rating =3, count = 10):
  p = rating
  n = count
  z = 3.8
  # square of test statistic for 95 confidence
  if(rating < 2.5):
    return p + (z**2)/(2*n) + (z *((p*(5-p) + z**2/(4*n))/n)**0.5)/(1+z**2/n)
  else:
    return p + (z**2)/(2*n) - (z *((p*(5-p) + z**2/(4*n))/n)**0.5)/(1+z**2/n)
