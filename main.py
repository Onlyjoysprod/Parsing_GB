import requests
import json

# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

url = 'https://api.github.com'
user = 'Onlyjoysprod'

req = requests.get(f'{url}/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(req.json(), f)

for tup in req.json():
    print(tup['name'])


# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

key = 'Sz1K4UkERRBE87RziC4scVuqtR30WSYaftzl1fLt'
service = f'https://api.nasa.gov/insight_weather/?api_key={key}&feedtype=json&ver=1.0'
req2 = requests.get(service)

with open('response.json', 'w') as f:
    json.dump(req2.json(), f)
