import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "video/1", json={"likes": 10, "name": "First Video", "views": 100})
print(response.json())

response = requests.get(BASE + "video/1")
print(response.json())