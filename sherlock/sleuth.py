from sherlock.integrations.fastapi import FastAPIIntegration
from sherlock.integrations.requests import RequestsIntegration


def _setup_integrations() -> None:
    # TODO: Add logic to detect installed libraries and accordingly set up the corresponding integrations.
    RequestsIntegration()
    FastAPIIntegration()


def sleuth() -> None:
    """
    This method sets up the integrations to propagate `X-Correlation-ID`
    across all the http requests.

    :return: None
    """
    _setup_integrations()
