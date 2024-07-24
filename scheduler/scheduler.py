from storage_handler.storage_handler import get_data
import schedule
import time
from weather_updates.weather_updates import send_weather_updates

def scheduler():
    print('scheduler')
    users = get_data('users.json')
    frequency_one_users = {key: details for key, details in users.items() if details["frequency"] == 1}
    frequency_two_users = {key: details for key, details in users.items() if details["frequency"] == 2}
    
    def task_once_a_day():
        for user_phone in frequency_one_users:
            send_weather_updates(user_phone, users[user_phone]['location'])
                
    def task_twice_a_day():
        print("Task twice")
        for user_phone in frequency_two_users:
            send_weather_updates(user_phone, users[user_phone]['location'])
            
    schedule.every().day.at("09:00").do(task_once_a_day)

    schedule.every().day.at("09:00").do(task_twice_a_day)
    schedule.every().day.at("18:00").do(task_twice_a_day)

    
    while True:
        schedule.run_pending()
        time.sleep(1)

