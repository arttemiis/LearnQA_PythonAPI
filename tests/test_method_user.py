import pytest
import random
import string
from datetime import datetime
from lib.assertions import Assertion
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Тестировние методов запросов")
class TestMethodUser(BaseCase):
    param_dara = {
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    }
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string
    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime('%m%d%Y%H%M$S')
        self.email = f"{base_part}{random_part}@{domain}"
        self.password = '123'
        self.username = 'learnqa'
        self.firstName = 'learnqa'
        self.lastName = 'learnqa'


    @allure.feature("Создание пользователя")
    @allure.story("Неполные данные в запросе")
    @allure.severity('minor')
    def test_incorrect_email(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime('%m%d%Y%H%M$S')
        email = f"{base_part}{random_part}{domain}"
        data = self.prepare_registration_data(email)
        response = MyRequests.post("user", data=data1)
        Assertion.assert_code_status(response, 400)
        assert response.text == "Invalid email format", f"The email format is correct '{email}'"

    @allure.feature("Создание пользователя")
    @allure.story("Неполные данные в запросе")
    @allure.severity('minor')
    @pytest.mark.parametrize('conditions', param_dara)
    def test_with_missing_parameter(self, conditions):
        if conditions == "password":
            self.password = ""
            data = {"password": {self.password}, "username": {self.username}, "firstName": {self.firstName}, "lastName": {self.lastName}, "email": {self.email}}
        if conditions == "username":
            self.username = ""
            data = {"password": {self.password}, "username": {self.username}, "firstName": {self.firstName}, "lastName": {self.lastName}, "email": {self.email}}
        if conditions == "firstName":
            self.firstName = ""
            data = {"password": {self.password}, "username": {self.username}, "firstName": {self.firstName}, "lastName": {self.lastName}, "email": {self.email}}
        if conditions == "lastName":
            self.lastName = ""
            data = {"password": {self.password}, "username": {self.username}, "firstName": {self.firstName}, "lastName": {self.lastName}, "email": {self.email}}
        if conditions == "email":
            self.email = ""
            data = {"password": {self.password}, "username": {self.username}, "firstName": {self.firstName}, "lastName": {self.lastName}, "email": {self.email}}
        response = MyRequests.post("user", data=data)
        print(response.text)
        Assertion.assert_code_status(response, 400)
        assert response.text == f"The value of '{conditions}' field is too short", f"The value of '{conditions}' not field is too short"

    @allure.feature("Создание пользователя")
    @allure.story("Некорректное имя пользователя")
    def test_short_username(self):
        short_username = 'A'
        data = {"password": {self.password}, "username": {short_username}, "firstName": {self.firstName},
                "lastName": {self.lastName}, "email": {self.email}}
        response = MyRequests.post("user", data=data)
        Assertion.assert_code_status(response, 400)
        print(response.text)

        assert response.text == "The value of 'username' field is too short", f"The value of 'username' is correct"

    @allure.feature("Создание пользователя")
    @allure.story("Некорректное имя пользователя")
    @allure.severity('minor')
    def test_long_username(self):
        short_username = self.generate_random_string(300)
        data = {"password": {self.password}, "username": {short_username}, "firstName": {self.firstName},
                "lastName": {self.lastName}, "email": {self.email}}
        response = MyRequests.post("user", data=data)
        Assertion.assert_code_status(response, 400)
        print(response.text)

        assert response.text == "The value of 'username' field is too long", f"The value of 'username' is correct"



