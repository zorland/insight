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


@app.route('/oldwork')
def old():
    return render_template('oldwork.html')


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

#some overrides for demos
  weatherClassOver = {}
  if(len(inputInfo) >1):
      if (inputInfo[1] == "hot"):
          weatherClassOver['hot'] = True
      if (inputInfo[1] == "cold"):
          weatherClassOver['cold'] = True
      if (inputInfo[1] == "rain"):
          weatherClassOver['rain'] = True
      if (inputInfo[1] == "cloud"):
          weatherClassOver['cloud'] = True
      if (inputInfo[1] == "sun"):
          weatherClassOver['sun'] = True



  cityName = goog_City(inputInfo[0])

  myWeather = Weather()
  myWeather.setValues(inputInfo[0], weatherClassOver)
#  print "testing"
#  print weatherClassOver
  weatherClassInfo =  myWeather.getWeather()
#  print weatherClassInfo


  weatherURL=  myWeather.getImage()
  latlngClass = myWeather.getLL()
  localWeather = myWeather.getForecast()


  yelp_findRest(latlngClass, weatherClassInfo)
  yelp_getRest(latlngClass)
  tuples = algo_MakePd(weatherClassInfo)



  rest1Info = tuples.sort("jacq", ascending= False).values[0]
  rest2Info = tuples.sort("jacq", ascending= False).values[1]
  rest3Info = tuples.sort("jacq", ascending= False).values[2]
  rest4Info = tuples.sort("jacq", ascending= False).values[3]
  
#  print restInfo
#  print session['q']

  return render_template('index2.html', rest1 = rest1Info, rest2 = rest2Info, rest3 = rest3Info, rest4 = rest4Info, cityName = cityName, place = session['q'],dayHigh = localWeather[0], dayCloudy= localWeather[1], weatherImage = weatherURL )
#  return render_template('results.html')


if __name__ == "__main__":



    app.run()
#    app.run(host="0.0.0.0",port=80)

    #hello() ??
