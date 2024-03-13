import unittest

import requests
import responses

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sleuth()

    @responses.activate
    def test_requests_integration(self):
        responses.get("https://markovml.com")

        response = requests.get("https://markovml.com")
        request = responses.calls[0].request

        self.assertIn(CORRELATION_ID_NAME, request.headers)
        self.assertIn(CORRELATION_ID_NAME, response.headers)
        self.assertEqual(200, response.status_code)
