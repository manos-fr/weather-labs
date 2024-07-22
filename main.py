import json
import time

from PythonSE105.messaging.storage_handler import load_data
from data_fetcher.data_fetcher import get_weather, get_messages
from message_handler.message_handler import send_sms
from storage_handler.storage_handler import get_data, save_data

# Constants definition
MESSAGE_API_ENDPOINT = "http://hackathons.masterschool.com:3030/POST/sms/send"
MESSAGE_FETCH_API = "http://hackathons.masterschool.com:3030/GET/team/getMessages"
WEATHER_API_URL = 'http://api.openweathermap.org/geo/1.0/direct?'
WEATHER_API_KEY = '6fd476d486aef7837462c558dfcaedc5'
PHONE_NUMBER = '491771786208'
SUBSCRIBE_MESSAGE = 'SUBSCRIBE THUNDERLABS'
JSON_FILE = "users.json"
API_CALL_INTERVAL = 240
#UPDATE_FREQUENCY = 3600 #daily fixed - need to handle this in the main

def sms_interaction(messages, users):
    for item in messages:
        user_phone = messages.get('phone_number')
        team_name = messages.get('team_name')

        #handle location
        if team_name == "SUBSCRIBE THUNDERLABS" and user_phone not in users:
            try:
                send_sms(user_phone, "sms your LOCATION", MESSAGE_API_ENDPOINT)#TO WRITE TO the post send sms
            except Exception as e:
                print(f"not a valid num {user_phone}: {e}")
                continue

        #first try the hardcoded location
        city_name = "Dublin"
        try:
            location = WEATHER_API_URL + "appid=" + WEATHER_API_KEY + "&q=" + city_name
            weather_data = get_weather(location)
            weather_description = weather_data['weather'][0]['description']
            forecast_message = f"The weather in the elected locatio {location} is {weather_description}."

            # Send weather forecast back to user
            send_sms(user_phone, forecast_message, MESSAGE_API_ENDPOINT)
            print("message sent")


            #some sort of update is needed probably

            #and a final save

        #need to add the time frequency to how often the api is called
        time.sleep(API_CALL_INTERVAL)
def main():
    print("Team Thunder Labs")
    print("Weather Labs")

    while True:
        #get messages
        messages= get_messages(MESSAGE_FETCH_API)
        time.sleep(API_CALL_INTERVAL)
        print("waiting...")
        users = get_data(JSON_FILE)
        sms_interaction(messages,users)
        time.sleep(API_CALL_INTERVAL)


if __name__ == "__main__":
    main()
