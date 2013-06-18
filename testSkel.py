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

  
  weatherLookup = nws_APICall(session['q'])
  match = nws_gatherInfo(weatherLookup)
  localWeather = nws_getLocal(match)

  weatherInfo = {}
  weatherInfo = nws_setWeather(localWeather)
  latlng = nws_getLL()

  yelp_findRest(latlng)
  yelp_getRest(latlng)

  tuples = algo_MakePd(weatherInfo)

  restInfo = tuples.sort("jacq", ascending= False).values[0]
  rest1Info = tuples.sort("jacq", ascending= False).values[1]
  rest2Info = tuples.sort("jacq", ascending= False).values[2]
  rest3Info = tuples.sort("jacq", ascending= False).values[3]
  
  print restInfo
  print session['q']

  return render_template('index2.html', place = session['q'], restDist = restInfo[1], restName = restInfo[2], restRating = restInfo[3], restUrl = restInfo[5], restCat = restInfo[8],restJacq = restInfo[10], rest1Dist = rest1Info[1], rest1Name = rest1Info[2], rest1Rating = rest1Info[3], rest1Url = rest1Info[5], rest1Cat = rest1Info[8],rest1Jacq = rest1Info[10], dayHigh = localWeather[0], dayCloudy= localWeather[1] )
#  return render_template('results.html')


if __name__ == "__main__":



    app.run()

    #hello() ??
