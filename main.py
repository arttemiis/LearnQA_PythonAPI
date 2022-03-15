from json.decoder import JSONDecodeError
import requests
payload = {"login": "secret_login","password":"secret_pass"}
headers= {"some_header": "123"}
response = requests.post("https://playground.learnqa.ru/api/show_all_headers", allow_redirects = True)

print(response.text)
print(response.headers)
python -m pytest -s Ex11_cookie.py
