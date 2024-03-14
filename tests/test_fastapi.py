import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME


class TestFastAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sleuth()

    def setUp(self):
        app = FastAPI()

        @app.get("/")
        async def hello_world():
            return {"msg": "Hello World"}

        self.client = TestClient(app)

    def test_fastapi_integration(self):
        response = self.client.get("/")
        self.assertIn(CORRELATION_ID_NAME.lower(), response.headers.keys())
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}
