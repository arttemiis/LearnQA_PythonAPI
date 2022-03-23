import time

import pytest
from datetime import datetime
import requests
from lib.assertions import Assertion
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Тестировние методов запросов")
class TestUserEdit(BaseCase):

    @allure.feature("Негативные тесты на Put")
    @allure.story("Неавторизованный запрос")
    @allure.description('Попытаемся изменить данные пользователя, будучи неавторизованными')
    @allure.severity('minor')
    def test_change_unauthorized_users(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("user", data=register_data)
        Assertion.assert_code_status(response, 200)
        Assertion.assert_json_has_key(response, "id")
        user_id = self.get_json_value(response, "id")
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"user/{user_id}",
            data={"firstName": new_name}
        )
        Assertion.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Auth token not supplied", "Auth token supplied"

    @allure.feature("Негативные тесты на Put")
    @allure.story("Неавторизованный запрос")
    @allure.description("Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем")
    @allure.severity('minor')
    def test_change_authorized_by_another_user(self):

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
        auth_sid_first = self.get_cookie(response2, "auth_sid")
        token_first = self.get_header(response2, "x-csrf-token")

        time.sleep(2)

        register_data2 = self.prepare_registration_data()
        response3 = MyRequests.post("user", data=register_data2)
        Assertion.assert_code_status(response3, 200)
        Assertion.assert_json_has_key(response3, "id")
        user_id_second = self.get_json_value(response3, "id")
        old_name = register_data2['firstName']
        email = register_data2['email']
        password = register_data2['password']

        auth_data_second = {
            'email': email,
            'password': password
        }
        response4 = MyRequests.post("user/login", data=auth_data_second)
        auth_sid_second = self.get_cookie(response4, "auth_sid")
        token_second = self.get_header(response4, "x-csrf-token")

        new_name = "Changed Name"
        response5 = MyRequests.put(
            f"user/{user_id_second}",
            headers={"x-csrf-token": token_first},
            cookies={"auth_sid": auth_sid_first},
            data={"firstName": new_name}
        )
        Assertion.assert_code_status(response5, 200)

        response6 = MyRequests.get(f"user/{user_id_second}", headers={"x-csrf-token": token_second},
                                   cookies={"auth_sid": auth_sid_second})

        Assertion.assert_json_value_by_name(response6, "firstName", old_name, "The value has changed")

    @allure.feature("Негативные тесты на Put")
    @allure.story("Авторизованный запрос")
    @allure.description("Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @")
    @allure.severity('minor')
    def test_change_your_email(self):
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
        base_part = "learnqa"
        domain = "example.com"
        time.sleep(1)
        random_part = datetime.now().strftime('%m%d%Y%H%M$S')
        new_email = f"{base_part}{random_part}{domain}"

        response3 = MyRequests.put(
            f"user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertion.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format", "Correct email format"

    @allure.feature("Негативные тесты на Put")
    @allure.story("Авторизованный запрос")
    @allure.description("Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ")
    @allure.severity('minor')
    def test_change_your_first_name_short(self):
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
        new_name = "P"

        response3 = MyRequests.put(
            f"user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertion.assert_code_status(response3, 400)
        Assertion.assert_json_value_by_name(response3, "error", "Too short value for field firstName", f"The new name has the correct format: '{new_name}'")


