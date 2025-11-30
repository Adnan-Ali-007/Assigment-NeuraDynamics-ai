import os
import requests
api_key = os.getenv('OPENWEATHER_API_KEY')
print('ENV KEY:', api_key)
resp = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q':'Chicago','appid':api_key,'units':'metric'})
print('STATUS', resp.status_code)
print(resp.text)
