from importlib import metadata as importlib_metadata
from typing import Dict, List

from sherlock.integrations.fastapi import FastAPIIntegration
from sherlock.integrations.httpx import HttpxIntegration
from sherlock.integrations.requests import RequestsIntegration
from sherlock.plugins.base_plugin import AbstractPlugin
from sherlock.plugins.sentry import SentryPlugin

_AVAILABLE_INTEGRATIONS: Dict = {
    RequestsIntegration.integration_type: RequestsIntegration,
    FastAPIIntegration.integration_type: FastAPIIntegration,
    HttpxIntegration.integration_type: HttpxIntegration,
}

_AVAILABLE_PLUGINS: Dict = {
    SentryPlugin.plugin_name: SentryPlugin,
}


def _attach_plugin(func, plugin: AbstractPlugin):
    def wrapper(*args, **kwargs):
        plugin.add_correlation_id()
        return func(*args, **kwargs)

    return wrapper


def _get_installed_libraries() -> List[str]:
    return [dist.metadata["Name"] for dist in importlib_metadata.distributions()]


def _setup_integrations() -> None:
    installed_libraries_set = set(_get_installed_libraries())
    available_libraries_integration_set = set(_AVAILABLE_INTEGRATIONS.keys())
    available_libraries_plugin_set = set(_AVAILABLE_PLUGINS.keys())

    integrations_to_use = installed_libraries_set.intersection(
        available_libraries_integration_set
    )
    plugins_to_use = installed_libraries_set.intersection(
        available_libraries_plugin_set
    )

    for integration_name in integrations_to_use:
        integration = _AVAILABLE_INTEGRATIONS[integration_name]
        integration_instance = integration()
        for plugin_name in plugins_to_use:
            plugin = _AVAILABLE_PLUGINS[plugin_name]
            integration_instance.new_send = _attach_plugin(
                integration_instance.new_send, plugin
            )
        integration_instance.add_patch()


def sleuth() -> None:
    """
    This method sets up the integrations to propagate `X-Correlation-ID`
    across all the http requests.

    :return: None value
    :rtype: None
    """
    _setup_integrations()
