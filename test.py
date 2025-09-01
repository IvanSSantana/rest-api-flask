import requests

BASE = "http://127.0.0.1:5000/"

# Testing the PUT Method
data = [{"likes": 10, "name": "First Video", "views": 100},
        {"likes": 9_421, "name": "Adding slime in my soup!", "views": 4_000_000},
        {"likes": 1000, "name": "WOW Signal! AMAZING!!!", "views": 2000}] 

for d in range(len(data)):
   try:
      response = requests.put(BASE + "video/" + str(d), json=data[d])
      print(response.json())
   except Exception as e:
      print(f"Error occurred: {e}")

input("Press Enter to continue...")

# Testing the GET Method
response = requests.get(BASE + "video/4")
print(response.json())

input("Press Enter to continue...")

# Testing the DELETE Method
response = requests.delete(BASE + "video/9")
print(response)

input("Press Enter to continue...")

# Testing the PATCH Method
response = requests.patch(BASE + "video/0", json={"likes": None, "views": 1})
print(response)