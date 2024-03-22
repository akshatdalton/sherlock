import unittest

import requests

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME


class TestRequestsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sleuth()

    def test_requests_integration(self):
        response = requests.get("https://google.com")
        self.assertIn(CORRELATION_ID_NAME, response.headers)
        self.assertEqual(200, response.status_code)
