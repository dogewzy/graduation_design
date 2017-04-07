from unittest import TestCase
import requests

class TestIndexHandler(TestCase):
    def test_get(self):
        rep = requests.get('localhost:8080')
        if rep:
            print rep
            assert 1==1
        assert 1==0

