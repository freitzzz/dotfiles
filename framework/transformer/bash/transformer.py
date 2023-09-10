from abc import abstractmethod
from typing import Generic

from framework.core.types import Converter, Factory, TI, Bash


class BashConverter(Converter[TI, Bash], Generic[TI]):
    """
    Types a :class:`Converter` that accepts :class:`TI` input and converts it in Bash output.
    """

    @abstractmethod
    def accepts(self, _input: TI) -> bool:
        ...

    @abstractmethod
    def convert(self, _input: TI) -> Bash:
        ...


class BashFactory(Factory[TI, Bash], Generic[TI]):
    """
    Types a :class:`Factory` that accepts :class:`TI` and converts it in Bash output.
    """
    pass
