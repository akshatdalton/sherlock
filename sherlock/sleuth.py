from importlib import metadata as importlib_metadata
from typing import Dict, List

from sherlock.integrations.fastapi import FastAPIIntegration
from sherlock.integrations.httpx import HttpxIntegration
from sherlock.integrations.requests import RequestsIntegration

AVAILABLE_INTEGRATIONS: Dict = {
    RequestsIntegration.integration_name: RequestsIntegration,
    FastAPIIntegration.integration_name: FastAPIIntegration,
    HttpxIntegration.integration_name: HttpxIntegration,
}


def _get_installed_libraries() -> List[str]:
    return [dist.metadata["Name"] for dist in importlib_metadata.distributions()]


def _setup_integrations() -> None:
    installed_libraries_set = set(_get_installed_libraries())
    available_libraries_integration_set = set(AVAILABLE_INTEGRATIONS.keys())

    for found_library in installed_libraries_set.intersection(
        available_libraries_integration_set
    ):
        integration = AVAILABLE_INTEGRATIONS[found_library]
        integration().add_patch()


def sleuth() -> None:
    """
    This method sets up the integrations to propagate `X-Correlation-ID`
    across all the http requests.

    :return: None
    """
    _setup_integrations()
