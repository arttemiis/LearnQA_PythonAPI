import requests
class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert response.status_code == 200, "Wrong response code"
        assert "x-secret-homework-header" in response.headers, "There is no header in the response"
        header = response.headers.get("x-secret-homework-header")
        print(header)
        assert header == "Some secret value", "The header value is incorrect"


