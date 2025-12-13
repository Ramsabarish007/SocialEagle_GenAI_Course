# modules
import requests
import time
import webbrowser

webbrowser.open("https://www.google.com")

time.sleep(5)
response = requests.get("https://www.google.com")
print("Response status code:", response.status_code)