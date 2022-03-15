import requests
class TestShortPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) >= 15, "The phrase contains less than 15 symbol"


