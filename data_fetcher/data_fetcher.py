import requests


#karim, please add your code below, i added this to test the main.  This works now, the messages are getting returned from the getMessageapi

def get_messages(api_endpoint, team_name):
    """Fetch Messages from getMessages API"""
    url = f"{api_endpoint}/{team_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching messages: {e}")
        if response:
            print("Response content:", response.content)
        raise

WEATHER_API_KEY = '6fd476d486aef7837462c558dfcaedc5'

def get_weather(lat,lon):
    """Fetch the weather from the weather API"""
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}


