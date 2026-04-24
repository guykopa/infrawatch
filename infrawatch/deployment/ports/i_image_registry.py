from abc import ABC, abstractmethod


class IImageRegistry(ABC):
    """Contract for container image registries."""

    @abstractmethod
    def push(self, image: str, tag: str) -> str: ...

    @abstractmethod
    def image_exists(self, image: str, tag: str) -> bool: ...
