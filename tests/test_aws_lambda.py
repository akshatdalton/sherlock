import unittest
from unittest.mock import MagicMock
from uuid import uuid4

from sherlock import sleuth
from sherlock.constants import CORRELATION_ID_NAME
from sherlock.integrations.aws_lambda import AWSLambdaIntegration


def lambda_handler(event, context):
    # Sample implementation: just return a hello message
    return {"statusCode": 200, "body": '{"message": "Hello from Lambda!"}'}


class TestAWSLambdaIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sleuth(
            extra_integrations=[
                AWSLambdaIntegration(
                    module_path=__name__, func_name=lambda_handler.__name__
                )
            ]
        )

    def test_aws_lambda_integration(self):
        event = {"key1": "value1", "key2": "value2"}
        context = MagicMock()

        response = lambda_handler(event, context)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn(CORRELATION_ID_NAME, response["headers"])

        correlation_id = uuid4().hex
        event["headers"] = {}
        event["headers"][CORRELATION_ID_NAME] = correlation_id

        response = lambda_handler(event, context)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn(CORRELATION_ID_NAME, response["headers"])
        self.assertEqual(response["headers"][CORRELATION_ID_NAME], correlation_id)
