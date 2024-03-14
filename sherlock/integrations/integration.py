from abc import ABC, abstractmethod


class AbstractIntegration(ABC):
    """
    All subclasses need to assign patched integration
    function to instance variable: `new_send`.

    To implement the patch for the integration,
    `add_patch` method will be called.
    """

    @abstractmethod
    def __init__(self) -> None:
        self.new_send = None

    @abstractmethod
    def add_patch(self) -> None:
        pass

    @property
    @abstractmethod
    def integration_name(self) -> str:
        pass
