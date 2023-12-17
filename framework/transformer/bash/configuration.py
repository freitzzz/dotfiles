from framework.core.func import join_lines
from framework.core.types import Bash
from framework.schema.configuration import GitConfigModule, AliasModule
from framework.schema.module import ModuleType
from framework.transformer.bash.module import ModuleConverter


class AliasModuleConverter(ModuleConverter[AliasModule]):
    """
    A :class:`ModuleConverter` for :class:`AliasModule`.
    """

    def convert(self, _input: AliasModule) -> Bash:
        return join_lines(
            [
                "alias_source=~/.bash_aliases",
                "touch $alias_source",
                "source $alias_source",
                *map(lambda e: f"alias {e[0]}='{e[1]}'", _input.entries.value.items()),
                "alias > $alias_source"
            ]
        )

    def module_type(self) -> ModuleType:
        return ModuleType.alias


class GitConfigModuleConverter(ModuleConverter[GitConfigModule]):
    """
    A :class:`ModuleConverter` for :class:`GitConfigModule`.
    """

    def convert(self, _input: GitConfigModule) -> Bash:
        return join_lines(map(lambda e: f"git config --global {e[0]} {e[1]}", _input.entries.value.items()))

    def module_type(self) -> ModuleType:
        return ModuleType.git_config
