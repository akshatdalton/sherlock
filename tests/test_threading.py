import concurrent.futures
import unittest

import requests
import responses

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME


class TestRequestsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sleuth()

    @responses.activate
    def test_threads_different_ids(self):
        responses.get("https://google.com")
        request_counter = 0

        def get_request_and_response():
            response = requests.get("https://google.com")
            request = responses.calls[request_counter].request
            return request, response

        request1, response1 = get_request_and_response()
        request_counter += 1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(get_request_and_response)
            request2, response2 = future.result()

        self.assertIn(CORRELATION_ID_NAME, request1.headers)
        self.assertIn(CORRELATION_ID_NAME, response1.headers)
        self.assertEqual(
            request1.headers.get(CORRELATION_ID_NAME),
            response1.headers.get(CORRELATION_ID_NAME),
        )
        self.assertEqual(200, response1.status_code)

        self.assertIn(CORRELATION_ID_NAME, request2.headers)
        self.assertIn(CORRELATION_ID_NAME, response2.headers)
        self.assertEqual(
            request2.headers.get(CORRELATION_ID_NAME),
            response2.headers.get(CORRELATION_ID_NAME),
        )
        self.assertEqual(200, response2.status_code)

        self.assertNotEquals(
            response1.headers.get(CORRELATION_ID_NAME),
            response2.headers.get(CORRELATION_ID_NAME),
        )
