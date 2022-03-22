import time

import pytest
from datetime import datetime
import requests
from lib.assertions import Assertion
from lib.my_requests import MyRequests
from lib.base_case import BaseCase

class TestUserDelete(BaseCase):
    def test_delete_vinkotov_user(self):

        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.put(
            "user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertion.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not edit test users with ID 1, 2, 3, 4 or 5.", "Deleted a user with an Id greater than 5"

    def test_delete_yourself(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("user", data=register_data)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data['email']
        password = register_data['password']

        auth_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("user/login", data=auth_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertion.assert_code_status(response3, 200)
        assert response3.content.decode("utf-8") == "", "Couldn't delete myself"

        response3 = MyRequests.get(
            f"user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertion.assert_code_status(response3, 404)
        assert response3.content.decode("utf-8") == "User not found", "The remote user exists!!"

    def test_delete_authorized_by_another_user(self):
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("user", data=register_data1)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, "id")
        user_id_first = self.get_json_value(response1, "id")
        email = register_data1['email']
        password = register_data1['password']

        auth_data_first = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("user/login", data=auth_data_first)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        time.sleep(1)

        register_data2 = self.prepare_registration_data()
        response3 = MyRequests.post("user", data=register_data2)
        Assertion.assert_code_status(response3, 200)
        Assertion.assert_json_has_key(response3, "id")
        user_id_second = self.get_json_value(response3, "id")

        response4 = MyRequests.delete(
            f"user/{user_id_second}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertion.assert_code_status(response4, 200)
        response5 = MyRequests.get(
            f"user/{user_id_second}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertion.assert_json_has_key(response5, "username")





