import pytest
import requests
from datetime import datetime
from lib.assertions import Assertion
from lib.my_requests import MyRequests
from lib.base_case import BaseCase

class TestMethodUser(BaseCase):


    def test_incorrect_email(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime('%m%d%Y%H%M$S')
        email = f"{base_part}{random_part}@{domain}"
        data = self.prepare_registration_data(email)
        response = MyRequests.post("user", data=data)
        Assertion.assert_code_status(response, 400)
        assert response.text == "Invalid email format", f"The email format is correct '{email}'"
