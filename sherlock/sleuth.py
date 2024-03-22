from importlib import metadata as importlib_metadata
from typing import Callable, Dict, List, Optional, Set

from sherlock.instrumentation import set_correlation_id_generator
from sherlock.integrations.aws_lambda import AWSLambdaIntegration
from sherlock.integrations.fastapi import FastAPIIntegration
from sherlock.integrations.httpx import HttpxIntegration
from sherlock.integrations.urllib3 import Urllib3Integration
from sherlock.plugins.base_plugin import AbstractPlugin
from sherlock.plugins.sentry import SentryPlugin

_AVAILABLE_INTEGRATIONS: Dict = {
    FastAPIIntegration.integration_type: FastAPIIntegration,
    HttpxIntegration.integration_type: HttpxIntegration,
    Urllib3Integration.integration_type: Urllib3Integration,
    AWSLambdaIntegration.integration_type: AWSLambdaIntegration,
}

_AVAILABLE_PLUGINS: Dict = {
    SentryPlugin.plugin_name: SentryPlugin,
}


def _attach_plugin(func, plugin: AbstractPlugin):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        plugin.add_correlation_id()
        return response

    return wrapper


def _add_plugins_to_integration(plugins_to_use: Set[str], integration):
    for plugin_name in plugins_to_use:
        plugin = _AVAILABLE_PLUGINS[plugin_name]
        integration.update_args_and_kwargs_with_request_headers = _attach_plugin(
            integration.update_args_and_kwargs_with_request_headers, plugin
        )
    return integration


def _get_installed_libraries() -> List[str]:
    return [dist.metadata["Name"] for dist in importlib_metadata.distributions()]


def _setup_integrations(extra_integrations: List) -> None:
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
        integration_cls = _AVAILABLE_INTEGRATIONS[integration_name]
        integration_instance = integration_cls()
        integration_instance = _add_plugins_to_integration(
            plugins_to_use, integration_instance
        )
        integration_instance.add_patch()

    for extra_integration in extra_integrations:
        integration_instance = _add_plugins_to_integration(
            plugins_to_use, extra_integration
        )
        integration_instance.add_patch()


def sleuth(
    correlation_id_generator_func: Optional[Callable[[], str]] = None,
    extra_integrations: Optional[List] = None,
) -> None:
    """
    This method sets up the integrations to propagate `X-Correlation-ID`
    across all the http requests.

    :param correlation_id_generator_func: Callable function to generate unique correlation ID.
            If passed `None`, hex value of uuid4 will be used as a generator.
    :type correlation_id_generator_func: Optional[Callable[[], str]]
    :param extra_integrations: Extra integrations to add.
            Example: AWSLambdaIntegration. Default is None.
    :type extra_integrations: Optional[List]
    :return: None value
    :rtype: None
    """
    extra_integrations = extra_integrations or []
    set_correlation_id_generator(correlation_id_generator_func)
    _setup_integrations(extra_integrations)
