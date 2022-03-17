import pytest
import requests
from lib.assertions import Assertion
from lib.base_case import BaseCase

class TestUserAuth(BaseCase):
    exlude_param =[
        ("no_cookie"),
        ("no_token")
    ]
    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'passvord': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid =self.get_cookie(response1,"auth-sid")
        self.token = self.get_header(response1, "x-csrf-token")
    def test_auth_user(self):
        response2 = requests.get("https://playground.learnqa.ru/api/users/auth",
        headers={"x-csrf-token": self.token},
        cookies={"auth_sid": self.auth_sid}
        )
        Assertion.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

