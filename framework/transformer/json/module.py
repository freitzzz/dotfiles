from abc import abstractmethod
from typing import TypeVar, Generic

from framework.core.types import JSON
from framework.schema.module import ModuleDependency, ModuleName, ModuleType, Module
from framework.transformer.json.transformer import JsonConverter, JsonFactory

M = TypeVar('M', bound=Module)


class ModuleDependencyConverter(JsonConverter[ModuleDependency]):
    """
    A :class:`JsonConverter` for :class:`ModuleDependency`.
    """

    def accepts(self, _input: JSON) -> bool:
        return (_input.get('type') and _input.get('name')) is not None

    def convert(self, _input: JSON) -> ModuleDependency:
        return ModuleDependency(
            ModuleType.of(_input.get('type')),
            ModuleName(_input.get('name')),
        )


class ModuleConverter(JsonConverter[M], Generic[M]):
    """
    Types a :class:`JsonConverter` for :class:`Module`.
    """

    def accepts(self, _input: JSON) -> bool:
        if (_input.get('name') == "personal"):
            print(
                f"yo ({_input.get('name')}): {_input.get('type')} and {self.module_type().value} == {_input.get('type') == self.module_type().value}")
            print(dict(_input))
        return _input.get('type') == self.module_type().value and _input.get('name') is not None

    @abstractmethod
    def module_type(self) -> ModuleType:
        """
        Describes the module to convert type.

        :return: the :class:`ModuleType` that describes this converter.
        """
        ...

    def __init__(self, dependency_converter: ModuleDependencyConverter) -> None:
        self.dependency_converter = dependency_converter


class ModuleFactory(JsonFactory[Module]):
    """
    Types a :class:`Factory` for :class:`Module`.
    """

    def __init__(self, converters: set[ModuleConverter]):
        super().__init__(converters)
