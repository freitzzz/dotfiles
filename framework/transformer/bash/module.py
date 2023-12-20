from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from framework.schema.module import Module, ModuleType
from framework.transformer.bash.transformer import BashConverter, BashFactory

M = TypeVar('M', bound=Module)


class ModuleConverter(BashConverter[M], Generic[M], ABC):
    """
    Types a :class:`BashConverter` for :class:`Module`.
    """

    def accepts(self, _input: M) -> bool:
        print(f"??? ({_input.name}) -> {_input.type}")
        print(dict(_input))
        return _input.type == self.module_type()

    @abstractmethod
    def module_type(self) -> ModuleType:
        """
        Describes the module to convert type.

        :return: the :class:`ModuleType` that describes this converter.
        """
        ...


class ModuleFactory(BashFactory[Module]):
    """
    Types a :class:`Factory` for :class:`Module`.
    """

    def __init__(self, converters: set[ModuleConverter]):
        super().__init__(converters)
