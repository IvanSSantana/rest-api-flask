from typing import List
from colorama import Fore
import requests

BASE = "http://127.0.0.1:5000/"

tests: List[bool] = []

def test_approved(response):
   if response.status_code in range(200, 299):
       tests.append(True)
   else:
       tests.append(False)

# Testing the PUT Method
data = [{"likes": 745, "name": "Test 1", "views": 453},
        {"likes": 9421, "name": "Test 2", "views": 543_563},
        {"likes": 31_231, "name": "Test 3", "views": 4242}] 

for d in range(len(data)):
   try:
      response = requests.put(BASE + "video/" + str(d + 10), json=data[d])
      print(response.json())
   except Exception as e:
      print(f"Error occurred: {e}")
   finally:
      test_approved(response)

input("Press Enter to continue...")

# Testing the GET Method
response = requests.get(BASE + "video/4")
print(response.json())
test_approved(response)

input("Press Enter to continue...")

# Testing the DELETE Method
response = requests.delete(BASE + "video/12")
print(response)
test_approved(response)

input("Press Enter to continue...")

# Testing the PATCH Method
response = requests.patch(BASE + "video/0", json={"likes": None, "views": 1})
print(response)
test_approved(response)

coverage: List[int] = [i for i in range(len(tests)) if tests[i] == True]

print(Fore.GREEN + f"Total coverage is: {len(coverage)} out of {len(tests)}")
print(Fore.GREEN + "The coverage's percent is: {:.2f}%".format(len(coverage) / len(tests) * 100))
