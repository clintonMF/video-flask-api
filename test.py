import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.put(BASE + 'video/5',
                        {"likes": 10, "name":"clinton", "views":1})
print(response.json())
input()
response = requests.put(BASE + 'video/4',
                        {"likes": 10, "name":"clinton", "views":1})
print(response.json())
input()
response = requests.delete(BASE + 'video/5')
print(response.json())
response = requests.get(BASE + 'video/5')
print(response.json())