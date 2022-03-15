import requests
class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(response.cookies)
        assert "HomeWork" in response.cookies, "There is no cookie in the response"
        cookie = response.cookies.get("HomeWork")
        print(cookie)
        assert cookie == "hw_value", "The cookie value is incorrect"


