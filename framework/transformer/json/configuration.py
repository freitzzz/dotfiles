from framework.core.types import JSON
from framework.schema.configuration import GitConfigModule, AliasModule, Entries
from framework.schema.module import ModuleType
from framework.transformer.json.module import ModuleConverter, ModuleDependencyConverter


class AliasModuleConverter(ModuleConverter[AliasModule]):
    """
    A :class:`ModuleConverter` for :class:`AliasModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.alias

    def convert(self, _input: JSON) -> AliasModule:
        return AliasModule(
            name=_input.get('name'),
            entries=Entries(_input.get('entries')),
            dependencies=self.dependency_converter.convert_multiple(
                _input.get('dependencies')
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter) -> None:
        super().__init__(dependency_converter)


class GitConfigModuleConverter(ModuleConverter[GitConfigModule]):
    """
    A :class:`ModuleConverter` for :class:`GitConfigModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.git_config

    def convert(self, _input: JSON) -> GitConfigModule:
        return GitConfigModule(
            name=_input.get('name'),
            entries=Entries(_input.get('entries')),
            dependencies=self.dependency_converter.convert_multiple(
                _input.get('dependencies')
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter) -> None:
        super().__init__(dependency_converter)
