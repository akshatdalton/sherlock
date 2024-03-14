from abc import ABC, abstractmethod


class AbstractPlugin(ABC):
    plugin_name: str = None

    @staticmethod
    @abstractmethod
    def add_correlation_id() -> None:
        pass
