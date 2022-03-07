import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects = True)
first_response = response.history[0]
last_response = response
print(len(response.history))
print(last_response.url)

