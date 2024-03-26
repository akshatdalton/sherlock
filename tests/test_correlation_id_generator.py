import unittest
from uuid import uuid4

import requests

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME


def custom_correlation_id_generator():
    return f"tr-{uuid4().hex}"


class TestCorrelationIDGeneratorIntegration(unittest.TestCase):
    def setUp(self):
        sleuth(correlation_id_generator_func=custom_correlation_id_generator)

    def tearDown(self):
        sleuth(correlation_id_generator_func=lambda: uuid4().hex)

    def test_custom_correlation_id_generator(self):
        response = requests.get("https://google.com")

        self.assertIn(CORRELATION_ID_NAME, response.headers)
        self.assertEqual(response.headers.get(CORRELATION_ID_NAME)[:3], "tr-")
        self.assertEqual(200, response.status_code)
