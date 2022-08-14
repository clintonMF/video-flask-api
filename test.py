import requests

BASE = 'http://127.0.0.1:5000/'

data = [{"likes": 10000, "name":"How to make REST APIs", "views":80000},
        {"likes": 5000, "name":"the death of the world", "views":2000},
        {"likes": 500000, "name":"Tanjiro and Giyu vs Akaza", "views":10000000}]


for i in range(len(data)):
    response = requests.put(BASE + 'video/' + str(i), data[i -3])
    print(response.json())
input()

response = requests.get(BASE + 'video/3')
print(response.json())

response = requests.delete(BASE + 'video/0')
print(response.json())
input()
response = requests.patch(BASE + 'video/0', data[0])
print(response.json())