import requests

methods_list = ["GET", "POST", "PUT", "DELETE"]

for i in methods_list:
    method = i
    response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": f"{method}"})
    response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    print(f"GET with method {method}: " + response_get.text)
    print(f"POST with method {method}: " + response_post.text)
    print(f"PUT with method {method}: " + response_put.text)
    print(f"DELETE with method {method}: " + response_delete.text)
    print()


