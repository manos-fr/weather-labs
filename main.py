import json
import time
import datetime
import requests

from PythonSE105.messaging.storage_handler import load_data
from data_fetcher.data_fetcher import get_weather, get_messages
from message_handler.message_handler import send_sms
from storage_handler.storage_handler import get_data, save_data

# Constants definition
TEAM_NAME = "THUNDERLABS"
MESSAGE_API_ENDPOINT = "http://hackathons.masterschool.com:3030/sms/send"
MESSAGE_FETCH_API = "http://hackathons.masterschool.com:3030/team/getMessages"
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER_API_KEY = '6fd476d486aef7837462c558dfcaedc5'
PHONE_NUMBER = '491771786208'
SUBSCRIBE_MESSAGE = f"SUBSCRIBE {TEAM_NAME}"
JSON_FILE = "users.json"
API_CALL_INTERVAL = 240


# UPDATE_FREQUENCY = 3600 #daily fixed - need to handle this in the main

def get_coordinates(city_name):
    """Fetch latitude and longitude for the given city name."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        print(f"No data found for city: {city_name}")
        return None, None


def sms_interaction(messages, users):
    for message in messages:
        user_phone = message.get('PHONE_NUMBER')
        text = message.get('TEXT')

        if user_phone not in users:
            if text == "SUBSCRIBE THUNDERLABS":
                # New subscriber - ask for location
                send_sms(user_phone, "Please reply with your city name using the format: LOCATION <CityName>",
                         MESSAGE_API_ENDPOINT)
                users[user_phone] = {
                    "location": None,
                    "weather": None,
                    "last_update": None
                }
                save_data(JSON_FILE, users)

        elif text.startswith("LOCATION"):
            # Handle location update
            parts = text.split(" ", 1)
            if len(parts) > 1:
                city_name = parts[1]  # Extract city name from the message
                users[user_phone]['location'] = city_name
                send_sms(user_phone, f"Location '{city_name}' received. You will get weather updates shortly.",
                         MESSAGE_API_ENDPOINT)
                save_data(JSON_FILE, users)
            else:
                send_sms(user_phone, "Error: Invalid LOCATION format. Please use 'LOCATION <CityName>'.",
                         MESSAGE_API_ENDPOINT)

def send_weather_updates(users):
    for user_phone, user_data in users.items():
        location = user_data["location"]
        if location:
            try:
                weather_url = f"{WEATHER_API_URL}appid={WEATHER_API_KEY}&q={location}"
                weather_data = get_weather(weather_url)
                print(weather_data)

                if 'weather' in weather_data and weather_data['weather']:
                    weather_description = weather_data['weather'][0]['description']
                    forecast_message = f"The weather in {location} is  {weather_description}"
                    print(forecast_message)
                    send_sms(user_phone, forecast_message, MESSAGE_API_ENDPOINT)
                    print(f"Weather update sent to {user_phone}")

                    user_data["last_update"] = datetime.datetime.now().isoformat()
                    user_data["weather"] = weather_data
                    save_data(JSON_FILE, users)
                else:
                    send_sms(user_phone, "Error: No weather data available.", MESSAGE_API_ENDPOINT)

            except requests.RequestException as e:
                print(f"Error fetching weather data for {user_phone}: {e}")
                send_sms(user_phone, "Error: Could not fetch weather data.", MESSAGE_API_ENDPOINT)

        time.sleep(API_CALL_INTERVAL)




def main():
    print("Team Thunder Labs")
    print("Weather Labs")

    while True:
        try:
            # get messages
            messages = get_messages(MESSAGE_FETCH_API, TEAM_NAME)
            print(messages)
        except Exception as e:
            print("Messages were not retrieved")
            time.sleep(API_CALL_INTERVAL)
            continue
        print("waiting...")

        users = get_data(JSON_FILE)
        sms_interaction(messages, users)
        send_weather_updates(users)
        time.sleep(API_CALL_INTERVAL)


if __name__ == "__main__":
    main()
