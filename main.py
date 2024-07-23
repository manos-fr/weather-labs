import json
import time
import datetime

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
    #loop through the messages
    for message in messages:
        user_phone = message.get('phone_number')
        team_name = message.get('team_name')

        #handle location
        if team_name == "SUBSCRIBE THUNDERLABS" and user_phone not in users:
            try:
                send_sms(user_phone, "sms your LOCATION", MESSAGE_API_ENDPOINT)#TO WRITE TO the post send sms
                users[user_phone] = {
                    "location": None,
                    "weather": None,
                    "last_update": None
                }
                save_data(JSON_FILE, users)
            except Exception as e:
                print(f"not a valid num {user_phone}: {e}")
                continue


#first try the hardcoded location
def send_weather_updates(users):
    for user_phone, user_data in users.items():
        if not user_data["location"]:
            continue

        try:
            location = user_data["location"]
            weather_url = f"{WEATHER_API_URL}?appid={WEATHER_API_KEY}&q={location}"
            weather_data = get_weather(weather_url)
            weather_description = weather_data['weather'][0]['description']
            forecast_message = f"The weather in the elected locatio {location} is {weather_description}."

            # Send weather forecast back to user
            send_sms(user_phone, forecast_message, MESSAGE_API_ENDPOINT)
            print("message sent")

            #some sort of update is needed probably
            # Update last update time and weather data
            user_data["last_update"] = datetime.now().isoformat()
            user_data["weather"] = weather_data
            save_data(JSON_FILE, users)
        except Exception as e:
            print(f"Error sending weather update to {user_phone}: {e}")

        #need to add the time frequency to how often the api is called
        time.sleep(API_CALL_INTERVAL)
def main():
    print("Team Thunder Labs")
    print("Weather Labs")

    while True:
        try:
            #get messages
            messages= get_messages(MESSAGE_FETCH_API)
        except Exception as e:
            print("Messages were not retrieved")
            time.sleep(API_CALL_INTERVAL)
            continue
        print("waiting...")


        users = get_data(JSON_FILE)
        sms_interaction(messages,users)
        send_weather_updates(users)
        time.sleep(API_CALL_INTERVAL)


if __name__ == "__main__":
    main()
