from abc import ABC, abstractmethod


class AbstractIntegration(ABC):
    integration_name: str = None

    @abstractmethod
    def __init__(self) -> None:
        pass
