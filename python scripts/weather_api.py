import json
import pandas as pd
import requests as rq

key = '358d36a532debff940ed10fe8c2d9a1e' # weather api key


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
def weather_needs(temperature,wind_speeds,weather_status,weather):
    need_temp, need_wind, need_rain = False, False, False
    temp1, temp2 = sum(temperature[:int(len(temperature)/2)])/(len(temperature)/2),sum(temperature[int(len(temperature)/2):])/(len(temperature)/2)
    wind1, wind2 = sum(wind_speeds[:int(len(wind_speeds)/2)])/(len(wind_speeds)/2),sum(wind_speeds[int(len(wind_speeds)/2):])/(len(wind_speeds)/2)
    if((temp1 <= 15.0) | (temp2 <= 15.0)):
            need_temp = True
    if((wind1 >= 12.5) | (wind2 >= 12.5)):
        need_wind = True
    for i in range(len(temperature)):
        if((weather_status[i] >= 200 & weather_status[i] <= 232) | (weather_status[i] >= 500 & weather_status[i] <= 622)):
            need_rain = True
        

    print("Average temp over the next 6 hours: ",temp1)
    print("Average wind over the next 6 hours: ",wind1)
    print("Current weather: " + weather[0])

    return need_temp, need_wind, need_rain




def weather_api():
    lat,lon = get_lat_lon()

    # Get the hourly forecast for the next 48 hours
    weather_call = rq.get('https://api.openweathermap.org/data/2.5/onecall?lat='+lat+'&lon='+lon+'&exclude=current,minutely,daily,alerts&units=metric&appid='+key)
    data = weather_call.json()['hourly']

    # Get key values from the weather data, namely the temperature, wind speeds and weather forecast (think rainy, sunny, etc.)
    temps=[]
    winds=[]
    weather=[]
    weatherIDs=[]
    for i in range(0,12):
        temps.append(data[i]['temp'])
        winds.append(data[i]['wind_speed'])
        weather.append(data[i]['weather'][0]['description'])
        weatherIDs.append(data[i]['weather'][0]['id'])

    need_temp, need_wind, need_rain = weather_needs(temps,winds,weatherIDs,weather)
    
    return need_temp,need_wind,need_rain

