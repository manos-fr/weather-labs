import time
import datetime
import asyncio
import threading

# from PythonSE105.messaging.storage_handler import load_data
from weather_updates.weather_updates import send_weather_updates
from data_fetcher.data_fetcher import get_messages
from message_handler.message_handler import send_sms
from scheduler.scheduler import scheduler
from storage_handler.storage_handler import get_data, save_data

# Constants definition
TEAM_NAME = "THUNDERLABS"
MESSAGE_API_ENDPOINT = "http://hackathons.masterschool.com:3030/sms/send"
MESSAGE_FETCH_API = "http://hackathons.masterschool.com:3030/team/getMessages"
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER_API_KEY = '6fd476d486aef7837462c558dfcaedc5'
# PHONE_NUMBER = '306986147950'
SUBSCRIBE_MESSAGE = f"SUBSCRIBE {TEAM_NAME}"
JSON_FILE = "users.json"
API_CALL_INTERVAL = 5 # seconds TODO change to 240

async def sms_interaction(messages, users):
    try:
        for message in messages:
            check_list = users.keys()

            numeric_keys = [str(key) for key in message.keys()]
            existence_checks = {
                str(key): key in check_list for key in numeric_keys}

            phone_dict = message.keys()
            
            user_phone = list(phone_dict)[0]

            if existence_checks[user_phone] is False:
                index = len(message.get(user_phone)) - 1
                text = message.get(user_phone)[index].get('text')

                if text == "SUBSCRIBE THUNDERLABS":
                    # New subscriber - ask for location
                    await send_sms(user_phone, "Please reply with your city name and the frequency of updates using the format: LOCATION <CityName> DAILY <1_or_2>",
                                   MESSAGE_API_ENDPOINT)

                elif text.startswith("LOCATION"):
                    print("Location and frequency received")
                    parts = text.split(" ", 4)
                    if len(parts) >= 3:
                        city_name = parts[1]
                        frequency = parts[3]
                        
                        await send_sms(user_phone, f"Location '{city_name}' and frequency {frequency} times daily received. You will get weather updates shortly.",
                                       MESSAGE_API_ENDPOINT)
                        await send_weather_updates(user_phone, city_name)
                        users[user_phone] = {
                            "location": None,
                            "last_update": None,
                            "frequency": 0
                        }
                        
                        users[user_phone]['location'] = city_name
                        users[user_phone]["last_update"] = datetime.datetime.now().isoformat()
                        users[user_phone]["frequency"] = frequency
                        save_data(JSON_FILE, users)
                    else:
                        await send_sms(user_phone, "Error: Invalid LOCATION format. Please use 'LOCATION <CityName>'.",
                                       MESSAGE_API_ENDPOINT)
    except Exception as e:
        print(e)



async def main():
    print("Team Thunder Labs")
    print("Weather Labs")
    
    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    while True:
        try:
            # get messages
            messages = get_messages(MESSAGE_FETCH_API, TEAM_NAME)
            users = get_data(JSON_FILE)
            await sms_interaction(messages, users)
        except Exception as e:
            print("Messages were not retrieved", {e})
            time.sleep(API_CALL_INTERVAL)
            continue
        print("waiting...")
        time.sleep(API_CALL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
