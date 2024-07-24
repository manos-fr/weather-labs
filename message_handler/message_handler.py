#wendy, please add your code here
import requests


def send_sms(phone_number, message, api_endpoint):
    """
        user_phone: the phone number to which the message will be sent
        forecast_message: the message to send
        MESSAGE_API_ENDPOINT: URL of the API
        return: JSON_FILE
        """
    try:
        payload = {
            'phoneNumber': phone_number,
            'message': message,
            'sender': 'THUNDERLABS'
        }

        # Send the POST request to the SMS API endpoint
        response = requests.post(api_endpoint, json=payload, timeout=5)
        print('send sms response', response.json())
        # Check for HTTP request errors
        response.raise_for_status()

        # Return the response data
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"not a valid message {phone_number}: {e}")
        return None

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
