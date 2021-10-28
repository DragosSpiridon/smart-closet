import json
import pandas as pd
import requests as rq

# Get the latitude and longitude based on IP address
def get_lat_lon():
    url = 'http://ipinfo.io/json'
    response = rq.get(url)
    data = response.json()

    location = str(data['loc']).split(",")
    lat = location[0]
    lon = location[1]

    return lat,lon

# Decide whether clothing should be appropriate for cold, wind and rain based on weather
def weather_needs(temperature,wind_speeds,weather_status):

    need_temp = True
    need_wind = True
    need_rain = True



    return need_temp, need_wind, need_rain

database = pd.read_csv("Clothes_database.csv") # import clothing items database
lat,lon = get_lat_lon()
key = '358d36a532debff940ed10fe8c2d9a1e'

# Get the hourly forecast for the next 48 hours
weather_call = rq.get('https://api.openweathermap.org/data/2.5/onecall?lat='+lat+'&lon='+lon+'&exclude=current,minutely,daily,alerts&units=metric&appid='+key)
data = weather_call.json()['hourly']

temps=[]
winds=[]
weather=[]
for i in range(0,12):
    temps.append(data[i]['temp'])
    winds.append(data[i]['wind_speed'])
    weather.append(data[i]['weather'][0]['description'])

need_temp, need_wind, need_rain = weather_needs(temps,winds,weather)

print(temps)
print(winds)
print(weather)