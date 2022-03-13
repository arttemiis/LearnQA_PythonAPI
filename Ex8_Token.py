import requests
import time
import json

key_list = ["seconds", "token", "error", "status", "result"]
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print("Создаем задачу")
parsing = json.loads(response.text)

if key_list[0] in parsing:
    second = parsing[key_list[0]]
    if key_list[1] in parsing:
        token = parsing[key_list[1]]
    else:
        print(f"Параметра  {key_list[1]} нет в ответе")
else:
    print(f"Параметра  {key_list[0]} нет в ответе")

print("Создана задача с токеном \'" + token + "\' и временем выполнения " + str(second) + " секунд")
print("Проверяем статус задачи")
response_token = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": f"{token}"})
parsing = json.loads(response_token.text)
if key_list[3] in parsing:
    status = parsing[key_list[3]]
else:
    print(f"Параметра  {key_list[3]} нет в ответе")
print("Получен статус задачи: \'" + status + "\' ")
print("Ждем время выполнения: " + str(second) + " секунд и проверяем статус и результат")
time.sleep(second)
response_result = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": f"{token}"})
parsing = json.loads(response_result.text)
if key_list[4] in parsing:
    result = parsing[key_list[4]]
    if key_list[3] in parsing:
        status = parsing[key_list[3]]
        print("Получен статус задачи: \'" + status + "\' ")
        print("Результат задачи: \'" + result + "\'")
    else:
        print(f"Параметра  {key_list[3]} нет в ответе")
else:
    print(f"Параметра  {key_list[4]} нет в ответе")



