import json
json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

obj = json.loads(json_text)
key = "messages"
if key in obj:
    obj2 = obj[key][len(obj)]
    key2 = "message"
    if key2 in obj2:
        print(obj2[key2])
    else:
        print(f"Ключа  {key2} нет в JSON")
else:
    print(f"Ключа  {key} нет в JSON")
