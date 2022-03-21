import pytest
import requests
from lib.assertions import Assertion
from lib.my_requests import MyRequests
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
        response1 = MyRequests.post("user/login", data=data)
        self.auth_sid = self.get_cookie(response1,"auth-sid")
        self.token = self.get_header(response1, "x-csrf-token")
    def test_auth_user(self):
        response2 = MyRequests.get("users/auth",
        headers={"x-csrf-token": self.token},
        cookies={"auth_sid": self.auth_sid}
        )
        Assertion.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )
class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("users", dsta=data)
        Assertion.assert_code_status(response, 200)
        Assertion.assert_json_has_key(response ,"id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("users", data=data)
        Assertion.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data
        response1 = MyRequests.post("users", data=register_data)

        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['passwoed']
        user_id =self.get_json_value(response1,'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("login", data=login_data)
        auth_sid = self.get_cookie(response2,"auth_sid")
        token = self.get_cookie(response2, "x-csrf-token")

        # EDIT
        new_name = "Change Name"
        response3 = MyRequests.put(
            f"user{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertion.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"user{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertion.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong Name of the user after edit"
        )

