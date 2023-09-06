from framework.core.types import MapElement
from framework.schema.module import ModuleType, Module, ModuleName, ModuleDependency


class Entries(MapElement):
    """
    A map of entries for defining a configuration.
    """
    pass


class ConfigurationModule(Module):
    """
    Represents a module that instructs how to configure something.

    Attributes:
        entries: a set of key-value entries that describe a configuration.
    """

    def __init__(
            self,
            entries: Entries,
            _type: ModuleType,
            name: ModuleName,
            dependencies: set[ModuleDependency] = None
    ) -> None:
        super().__init__(_type, name, dependencies)

        self.entries = entries


class AliasModule(ConfigurationModule):
    """
    Represents a :class:`Module` to configure a session alias.
    """

    def __init__(self, entries: Entries, name: ModuleName, dependencies: set[ModuleDependency]):
        super().__init__(entries, ModuleType.alias, name, dependencies)


class GitConfigModule(ConfigurationModule):
    """
    Represents a :class:`Module` to configure Git tool.
    """

    def __init__(self, entries: Entries, name: ModuleName, dependencies: set[ModuleDependency]):
        super().__init__(entries, ModuleType.git_config, name, dependencies)
