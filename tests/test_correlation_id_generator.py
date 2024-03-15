import unittest
from uuid import uuid4

import requests
import responses

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME


def custom_correlation_id_generator():
    return f"tr-{uuid4().hex}"


class TestCorrelationIDGeneratorIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sleuth(correlation_id_generator_func=custom_correlation_id_generator)

    @responses.activate
    def test_custom_correlation_id_generator(self):
        responses.get("https://google.com")

        response = requests.get("https://google.com")
        request = responses.calls[0].request

        self.assertIn(CORRELATION_ID_NAME, request.headers)
        self.assertIn(CORRELATION_ID_NAME, response.headers)
        self.assertEqual(request.headers.get(CORRELATION_ID_NAME)[:3], "tr-")
        self.assertEqual(response.headers.get(CORRELATION_ID_NAME)[:3], "tr-")
        self.assertEqual(200, response.status_code)
