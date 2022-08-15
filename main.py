import requests
from datetime import datetime
from dotenv import dotenv_values


config = dotenv_values('.env')

API_KEY = config.get('API_KEY')
APP_ID = config.get('APP_ID')
EXERCISE_URL = config.get('EXERCISE_URL')
SHEETY_API = config.get('SHEETY_API')
SHEETY_TOKEN = config.get('SHEETY_TOKEN')
SHEETY_USERNAME = config.get('SHEETY_USERNAME')
AGE = config.get('AGE')


headers_post_exercise = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'Content-Type': 'application/json'
}

headers_post_sheety = {
    'Authorization': SHEETY_TOKEN
}


def create_a_record():
    return send_post_request(f'{SHEETY_API}{SHEETY_USERNAME}/myWorkouts/workouts',
                             create_a_record_sheety_params, headers_post_sheety)


def send_post_request(endpoint, params, headers):
    response = requests.post(url=endpoint, json=params, headers=headers)
    response.raise_for_status()
    return response.json()


def create_an_exercise():
    return send_post_request(f'{EXERCISE_URL}natural/exercise', create_exercise_params, headers_post_exercise)


today = datetime.now()
user_input = input('Enter the exercise you did today\n')
create_exercise_params = {
    "query": user_input,
    "gender": "male",
    "weight_kg": 76,
    "height_cm": 167,
    "age": AGE
}
data_exercise = create_an_exercise()

if len(data_exercise['exercises']) > 0:
    for data in data_exercise['exercises']:
        create_a_record_sheety_params = {
            'workout': {
                'date': today.strftime('%d/%m/%Y'),
                'time': today.strftime('%H:%M:%S'),
                'exercise': data['name'].title(),
                'duration': data['duration_min'],
                'calories': data['nf_calories']
            }
        }
        sheety_record = create_a_record()
