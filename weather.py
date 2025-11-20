import os
import pprint
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(lat=None, lon=None):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    return response.json()


if __name__ == "__main__":
    city = "Moscow"
    lat = 55.75222
    lon = 37.61556
    weather = get_weather(lat, lon)
    print(f"Weather in city {city}:")
    pprint.pprint(weather)