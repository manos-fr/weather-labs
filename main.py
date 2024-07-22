import json
import requests
from data_fetcher import *
from message_handler import *
from storage_handler import *

# Constants definition
MESSAGE_API_ENDPOINT = "ttp://hackathons.masterschool.com:3030/POST/sms/send"
MESSAGE_FETCH_API = "ttp://hackathons.masterschool.com:3030/GET/team/getMessages"
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_API_KEY = '6fd476d486aef7837462c558dfcaedc5'
PHONE_NUMBER = '491771786208'
SUBSCRIBE_MESSAGE = 'SUBSCRIBE THUNDERLABS'
JSON_FILE = "subscribers.json"

def main():
    messages = get_messages(MESSAGE_FETCH_API)
    subscribers = load_data(JSON_FILE)
    #wrap in a loop ensuring constant calls
    while True:
        for item in messages:
            user_phone = messages.get('phone_number')
            team_name = messages.get('team_name')

        #handle location
            if team_name == "SUBSCRIBE THUNDERLABS" and user_phone not in subscribers:
                try:
                    send_sms(user_phone, "Add your LOCATION", MESSAGE_API_ENDPOINT)#TO WRITE TO the post send sms
                except Exception as e:
                    print(f"not a valid num {user_phone}: {e}")
                    continue

        #first try the hardcoded location
        location = "Dublin"
        weather_data = get_weather(location, API_KEY)
        weather_description = weather_data['weather'][0]['description']
        forecast_message = f"The weather in the elected locatio {location} is {weather_description}."

        # Send weather forecast back to user
        send_sms(user_phone, forecast_message, MESSAGE_API_ENDPOINT)
