from abc import ABC, abstractmethod

from sherlock.constants import PluginTypes


class AbstractPlugin(ABC):
    @staticmethod
    @abstractmethod
    def add_correlation_id() -> None:
        pass

    @property
    @abstractmethod
    def plugin_name(self) -> PluginTypes:
        pass
