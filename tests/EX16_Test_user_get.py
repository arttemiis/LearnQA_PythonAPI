import pytest
from datetime import datetime
import requests
from lib.assertions import Assertion
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
class TestUserGet(BaseCase):

    def test_get_another_users_data(self):
        first_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("user/login", data=first_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_first = self.get_json_value(response1, "user_id")


        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("user", data=register_data)
        Assertion.assert_code_status(response2, 200)
        Assertion.assert_json_has_key(response2, "id")
        user_id_second = self.get_json_value(response2, "id")

        response3 = MyRequests.get(f"user/{user_id_second}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertion.assert_json_has_key(response3, "username")
        Assertion.assert_json_has_not_key(response3, "email")
        Assertion.assert_json_has_not_key(response3, "firstName")
        Assertion.assert_json_has_not_key(response3, "lastName")
