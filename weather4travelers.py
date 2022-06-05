"""
@author: Eduardo Islas
"""

import requests
import pandas as pd
import creds
from datetime import datetime

# Get tickets from CSV
csv_data = pd.read_csv("challenge_dataset.csv")
# Extract relevant data from dataset and convert to dictionary
data = csv_data[["origin_latitude","origin_longitude", "destination_latitude", "destination_longitude"]]
# Initialize cache
cache = dict()

# Get weather from cache
def get_weather(url):
    if url not in cache:
        cache[url] = get_weather_from_API(url)
    return cache[url]

# Get weather from API
def get_weather_from_API(url):
    try:
        response = requests.get(url) 
        if response.status_code != 200:
            raise
        else:
            return response.json()
    except Exception:
        print(f'An error has ocurred: {response.status_code}')

# Format the report    
def get_report(result):
    df_output = pd.DataFrame()   
    df_output["Flight number"] = csv_data["flight_num"]
    df_output["Airline"] = csv_data["airline"]
    df_output["Origin"] = csv_data["origin"]
    df_output["Origin Airport"] = csv_data["origin_name"]
    df_output["Temperature origin"] = result["weather_origin"]
    df_output["Destination"] = csv_data["destination"]
    df_output["Destination Airport"] = csv_data["destination_name"]
    df_output["Temperature destination"] = result["weather_destination"]
    return df_output

# Execute program
result = []
for i in data.index:
        url_origin = f'https://api.openweathermap.org/data/2.5/weather?lat={data["origin_latitude"][i]}&lon={data["origin_longitude"][i]}&units=metric&appid={creds.API_KEY}'
        url_destination = f'https://api.openweathermap.org/data/2.5/weather?lat={data["destination_latitude"][i]}&lon={data["destination_longitude"][i]}&units=metric&appid={creds.API_KEY}'
        weather_origin = get_weather(url_origin)
        weather_destination = get_weather(url_destination)
        if weather_origin != None and weather_destination != None:
            result.append({'weather_origin': weather_origin["main"]["temp"],'weather_destination': weather_destination["main"]["temp"]})

if len(result) > 0:
    output = get_report(pd.DataFrame(result))
    today = datetime.today().strftime('%d-%m-%Y')
    output.to_csv(f'report_{today}.csv', index=False)
    print("Report created")
else:
    print("Runtime error, report can not be created")