from abc import abstractmethod
from typing import Generic

from framework.core.types import Converter, JSON, TO, Factory


class JsonConverter(Converter[JSON, TO], Generic[TO]):
    """
    Types a :class:`Converter` that accepts JSON input and converts it in :class:`TO` output.
    """

    @abstractmethod
    def accepts(self, _input: JSON) -> bool:
        ...

    @abstractmethod
    def convert(self, _input: JSON) -> TO:
        ...


class JsonFactory(Factory[JSON, TO], Generic[TO]):
    """
    Types a :class:`Factory` that accepts JSON input and converts it in :class:`TO` output.
    """
    pass
