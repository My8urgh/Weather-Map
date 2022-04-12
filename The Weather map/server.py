# How to run this server in the background:
# =========================================
# Install flask (if not done already): pip install flask
# Install flask_cors (if not done already): pip install flask_cors
# In the Windows Command Prompt (not Visual Studio Code Terminal or PowerShell), navigate
# to the folder containing this server.py file.
# Type the following command to inform Flask to use this server.py file: set FLASK_APP=server
# Type the following command to start Flask: flask run
# After using the server, Press Cntrl+C to stop it.

# Use the datetime timedelta classes to create, extract and manupulate dates and times
from datetime import datetime, timedelta 
# Use json to format your response data
import json 
# Import the requests library to be able to SEND requests 
import requests

# From the flask library, import only the Flask, request and Response classes.
# The request class (not the same as the requests library) is used to RECEIVE requests
# If you have to convert several objects as one nested json structure, you cannot use flask.jsonify.
# Is such case, import json and flask.Response to create your own response. You will also
# need to set the response headers yourself e.g.:
#     return Response(json.dumps(jsonStructure), mimetype='application/json')
from flask import Flask, request, Response

# From the flask_cors library, import the CORS and cross_origin classes.
# These classes are used to prevent CORS errors.
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
@app.route("/", methods=["POST"]) # Run this method when receiving any POST request
@cross_origin(origin='*') # Allow requests from any domain
def myMainFunction():
    try:
        client_json_data = request.json
        #client_json_data = request.args
        weatherList = getWeather(client_json_data)
        return Response(json.dumps(weatherList), mimetype='application/json')
    except Exception as e:
        print(e)
        
def getWeather(client_json_data):
    
    lat = client_json_data['lat']
    lng = client_json_data['lng']
    location = str(lat) + ", " + str(lng)
    
    url = 'https://api.tomorrow.io/v4/timelines'
    
    querystring = {
    "location": location,
    "fields":["temperature", "cloudCover", "windSpeed", "windDirection"],
    "units":"metric",
    "timesteps":"1h",
    "apikey":"nlYb3yEebLBygaCUuNpHEHkx9xBN9j4C"}

    headers = {"Accept":"application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    my_data = response.json()['data']['timelines'][0]['intervals']
    
    weatherList = []
    for f in range(12):
        weather_data = my_data[f]

        # Extract the UTC date and time from 'startTime'
        # Characters 0-10 represents the date.
        # Characters 11-19 repesents the time
        utc_date = weather_data['startTime'][0:10]
        utc_time = weather_data['startTime'][11:19]
        
        utc_datetime_str = utc_date + " " + utc_time
        utc_datetime_obj = datetime.strptime(utc_datetime_str, '%Y-%m-%d %H:%M:%S')
        
        hours_added = timedelta(hours = 2)
        local_datetime_obj = utc_datetime_obj + hours_added
        
        local_date = local_datetime_obj.date()
        local_time = local_datetime_obj.time()
        
        # Extract and round the weather data from 'values'
        temperature     = round(weather_data['values']['temperature'])
        cloudcover      = round(weather_data['values']['cloudCover'])
        windSpeed       = round(weather_data['values']['windSpeed'])
        windDirection   = round(weather_data['values']['windDirection'])
        
        data_dict = {
            "date": local_date, 
            "time": local_time,
            "temp": temperature,
            "cloudcover": cloudcover,
            "windSpeed": windSpeed,
            "windDirection": windDirection
            }
        
        json_string = json.dumps(data_dict, default=str)
        
        json_object = json.loads(json_string)
            
        weatherList.append(json_object)
        
    return weatherList