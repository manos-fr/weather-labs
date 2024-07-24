import requests
from message_handler.message_handler import send_sms
from data_fetcher.data_fetcher import get_weather

WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER_API_KEY = '6fd476d486aef7837462c558dfcaedc5'
MESSAGE_API_ENDPOINT = "http://hackathons.masterschool.com:3030/sms/send"

async def send_weather_updates(user_phone, city_name):
    if city_name:
        try:
            weather_url = f"{WEATHER_API_URL}appid={WEATHER_API_KEY}&q={city_name}"
            weather_data = get_weather(weather_url)

            if 'weather' in weather_data and weather_data['weather']:
                weather_description = weather_data['weather'][0]['description']
                forecast_message = f"The weather in {city_name} is  {weather_description}"
                await send_sms(user_phone, forecast_message,
                               MESSAGE_API_ENDPOINT)
                print(f"Weather update sent to {user_phone}")
                
            else:
                await send_sms(
                    user_phone, "Error: No weather data available.", MESSAGE_API_ENDPOINT)

        except requests.RequestException as e:
            print(f"Error fetching weather data for {user_phone}: {e}")
            await send_sms(
                user_phone, "Error: Could not fetch weather data.", MESSAGE_API_ENDPOINT)
    else:
        await send_sms(user_phone, "Error: No location set. Please reply with 'LOCATION <CityName>' to set your location.",
                       MESSAGE_API_ENDPOINT)