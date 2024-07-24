import requests
import os
from dotenv import load_dotenv


#karim, please add your code below, i added this to test the main.  This works now, the messages are getting returned from the getMessageapi
load_dotenv()  #  Loads API_KEY from dotfile


def get_weather(city):
    # Get weather data from api and return dictionary
    API_KEY = os.getenv("WEATHER_API_KEY")
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(api_url).json()
    return response


