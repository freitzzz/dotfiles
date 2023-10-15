from typing import TypeVar, Generic

from framework.core.types import JSON
from framework.schema.profile import Profile, ProfileIdentifier
from framework.transformer.json import ModuleDependencyConverter
from framework.transformer.json.transformer import JsonConverter, JsonFactory

P = TypeVar('P', bound=Profile)

ModuleDefinitionConverter = ModuleDependencyConverter


class ProfileConverter(JsonConverter[P], Generic[P]):
    """
    Types a :class:`JsonConverter` for :class:`Profile`.
    """

    def convert(self, _input: JSON) -> Profile:
        return Profile(
            name=ProfileIdentifier(_input.get('name')),
            modules=self.definition_converter.convert_multiple(
                _input.get('modules')
            )
        )

    def accepts(self, _input: JSON) -> bool:
        return _input.get('name') is not None

    def __init__(self, definition_converter: ModuleDefinitionConverter) -> None:
        self.definition_converter = definition_converter


class ProfileFactory(JsonFactory[Profile]):
    """
    Types a :class:`Factory` for :class:`Profile`.
    """

    def __init__(self, converters: set[ProfileConverter]):
        super().__init__(converters)
