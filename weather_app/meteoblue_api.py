import requests
from config import METEOBLUE_API_KEY

def get_weather_data(latitude, longitude):
    url = f"https://my.meteoblue.com/packages/basic-day?apikey={METEOBLUE_API_KEY}&lat={latitude}&lon={longitude}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
