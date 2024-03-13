from abc import ABC, abstractmethod


class AbstractIntegration(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def integration_name(cls) -> str:
        pass
