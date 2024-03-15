from abc import ABC, abstractmethod

from sherlock.constants import IntegrationTypes


class AbstractIntegration(ABC):
    """
    All subclasses need to assign patched integration
    function to instance variable: `new_send`.

    To implement the patch for the integration,
    `add_patch` method will be called.
    """

    @abstractmethod
    def __init__(self) -> None:
        """
        Define new patch method and assign it to `new_send` variable.
        """
        self.new_send = None

    @abstractmethod
    def add_patch(self) -> None:
        """
        Call this method to apply the patch stored in `new_send` variable.
        """
        pass

    @property
    @abstractmethod
    def integration_type(self) -> IntegrationTypes:
        """
        Returns integration types.
        """
        pass
