from contextlib import closing
from flask import Flask, render_template, session, request, redirect, url_for
from nws import *
import requests
from location import *
from yelp import *
from algos import *
from pandas import *
from googDat import *

app = Flask(__name__)
app.secret_key = os.urandom(123456)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/slides')
def slides():
    return render_template('slides.html')

@app.route("/query.html", methods=['POST'])
def query():
    session['q'] = request.form['q']
    return redirect(url_for('results'))
 
@app.route("/results.html")
def results():
  if not 'q' in session:
    return render_template('index.html')
 
#  os.system("rm *.json")

  inputInfo = session['q'].split()
  #just zipcode and over-ride for now

  cityName = goog_City(inputInfo[0])

  myWeather = Weather()
  myWeather.setValues(inputInfo[0])

  weatherClassInfo =  myWeather.getWeather()
  weatherURL=  myWeather.getImage()
  latlngClass = myWeather.getLL()
  localWeather = myWeather.getForecast()


#some overrides for demos
  if(len(inputInfo) >1):
      if (inputInfo[1] == "hot"):
          weatherClassInfo['hot'] = True
      if (inputInfo[1] == "cold"):
          weatherClassInfo['cold'] = True
      if (inputInfo[1] == "rain"):
          weatherClassInfo['rain'] = True
      if (inputInfo[1] == "cloud"):
          weatherClassInfo['cloud'] = True
      if (inputInfo[1] == "sun"):
          weatherClassInfo['sun'] = True



  yelp_findRest(latlngClass, weatherClassInfo)
  yelp_getRest(latlngClass)
  tuples = algo_MakePd(weatherClassInfo)



  restInfo = tuples.sort("jacq", ascending= False).values[0]
  rest1Info = tuples.sort("jacq", ascending= False).values[1]
  rest2Info = tuples.sort("jacq", ascending= False).values[2]
  rest3Info = tuples.sort("jacq", ascending= False).values[3]
  
  print restInfo
  print session['q']

  return render_template('index2.html', cityName = cityName, place = session['q'], restDist = restInfo[1], restName = restInfo[2], restRating = restInfo[3], restUrl = restInfo[5], restCat = restInfo[8],restJacq = restInfo[10], rest1Dist = rest1Info[1], rest1Name = rest1Info[2], rest1Rating = rest1Info[3], rest1Url = rest1Info[5], rest1Cat = rest1Info[8],rest1Jacq = rest1Info[10],rest2Dist = rest2Info[1], rest2Name = rest2Info[2], rest2Rating = rest2Info[3], rest2Url = rest2Info[5], rest2Cat = rest2Info[8],rest2Jacq = rest2Info[10], rest3Dist = rest3Info[3], rest3Name = rest3Info[2], rest3Rating = rest3Info[3], rest3Url = rest3Info[5], rest3Cat = rest3Info[8],rest3Jacq = rest3Info[10],dayHigh = localWeather[0], dayCloudy= localWeather[1], weatherImage = weatherURL )
#  return render_template('results.html')


if __name__ == "__main__":



    app.run()
#    app.run(host="0.0.0.0",port=80)

    #hello() ??
