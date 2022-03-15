from json.decoder import JSONDecodeError
import requests
json_text = {"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}

response = requests.post("https://playground.learnqa.ru/api/show_all_headers", headers = headers)
json_parsing =
print(response.text)
print(response.headers)
