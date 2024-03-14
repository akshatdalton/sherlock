import unittest
from http import HTTPStatus

import httpx

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME


class TestHttpxIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sleuth()

    def test_httpx_integration(self):
        test_client = httpx.Client(
            transport=httpx.MockTransport(lambda request: httpx.Response(HTTPStatus.OK))
        )
        response = test_client.get("https://google.com")

        self.assertIn(CORRELATION_ID_NAME, response.headers)
        self.assertEqual(200, response.status_code)
