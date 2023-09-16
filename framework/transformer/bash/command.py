from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from framework.core.func import first, join_lines, safe_string, get_or_else, join
from framework.core.types import Bash
from framework.schema.command import \
    CommandAPT, CommandBash, CommandNPM, \
    CommandCopy, CommandRemove, CommandUnZip, CommandGunZip, CommandDartPub, CommandSDKMan, CommandType, CommandWget
from framework.schema.command import CommandModule, Command
from framework.schema.module import ModuleType
from framework.transformer.bash.module import ModuleConverter
from framework.transformer.bash.transformer import BashConverter

C = TypeVar('C', Command, Command)


def sudo(_input: Command, _output: Bash) -> Bash:
    """
    Applies sudo prefix to a command bash output if needed.

    :param _input: the command that may be required to run in sudo.
    :param _output: the output bash script, converted from the command
    :return: the bash script that runs in sudo if required.
    """
    return f"sudo {_output}" if _input.sudo else _output


def or_result(_input: str | None) -> Bash:
    """
    Returns either the input or the latest command result value if the input is None.

    :param _input: the input in comparison
    :return: the input or the latest command result value.
    """

    return get_or_else(_input, lambda: '"$result"')


class CommandConverter(BashConverter[C], Generic[C], ABC):
    """
    Types a :class:`BashConverter` for :class:`Command`.
    """

    @abstractmethod
    def command_type(self) -> CommandType:
        ...

    def accepts(self, _input: C) -> bool:
        return _input.type == self.command_type()


class CommandAPTConverter(CommandConverter[CommandAPT]):
    """
    A :class:`CommandConverter` for :class:`CommandAPT`.
    """

    def convert(self, _input: CommandAPT) -> Bash:
        install_commands = [
            *map(lambda r: f"sudo add-apt-repository {r}", _input.repositories),
        ]

        if _input.package is not None:
            install_commands.append(
                f"sudo apt-get install -y {_input.package}"
            )
        else:
            temp_deb_fp = f"/tmp/{hash(_input.url)}.deb"

            install_commands.extend(
                [
                    f"wget {_input.url} -O {temp_deb_fp}",
                    f"sudo apt-get install -y {temp_deb_fp}"
                ]
            )

        return join_lines(install_commands)

    def command_type(self) -> CommandType:
        return CommandType.apt


class CommandBashConverter(CommandConverter[CommandBash]):
    """
    A :class:`CommandConverter` for :class:`CommandBash`.
    """

    def convert(self, _input: CommandBash) -> Bash:
        return sudo(
            _input,
            join_lines(_input.source) if len(_input.source > 0) else f"wget -qO- {_input.url} | bash"
        )

    def command_type(self) -> CommandType:
        return CommandType.bash


class CommandCopyConverter(CommandConverter[CommandCopy]):
    """
    A :class:`CommandConverter` for :class:`CommandCopy`.
    """

    def convert(self, _input: CommandCopy) -> Bash:
        return f"sudo wget {_input.url} -P {_input.target}"

    def command_type(self) -> CommandType:
        return CommandType.copy


class CommandDartPubConverter(CommandConverter[CommandDartPub]):
    """
    A :class:`CommandConverter` for :class:`CommandDartPub`.
    """

    def convert(self, _input: CommandDartPub) -> Bash:
        return sudo(
            _input,
            f"dart pub global activate {_input.package}"
        )

    def command_type(self) -> CommandType:
        return CommandType.dart_pub


class CommandGunZipConverter(CommandConverter[CommandGunZip]):
    """
    A :class:`CommandConverter` for :class:`CommandGunZip`.
    """

    def convert(self, _input: CommandGunZip) -> Bash:
        source = or_result(_input.source)

        return join_lines(
            [
                f"cd {_input.target}",
                sudo(_input, f"tar -czvf {source}") if _input.tar else sudo(_input, f"gunzip {source}")
            ]
        )

    def command_type(self) -> CommandType:
        return CommandType.gunzip


class CommandNPMConverter(CommandConverter[CommandNPM]):
    """
    A :class:`CommandConverter` for :class:`CommandNPM`.
    """

    def convert(self, _input: CommandNPM) -> Bash:
        return sudo(
            _input,
            f"sudo npm install -g {_input.package}"
        )

    def command_type(self) -> CommandType:
        return CommandType.npm


class CommandRemoveConverter(CommandConverter[CommandRemove]):
    """
    A :class:`CommandConverter` for :class:`CommandRemove`.
    """

    def convert(self, _input: CommandRemove) -> Bash:
        return sudo(
            _input,
            f"rm -rf {_input.target}"
        )

    def command_type(self) -> CommandType:
        return CommandType.rm


class CommandSDKManConverter(CommandConverter[CommandSDKMan]):
    """
    A :class:`CommandConverter` for :class:`CommandSDKMan`.
    """

    def convert(self, _input: CommandSDKMan) -> Bash:
        return sudo(
            _input,
            f"sdk install {_input.package} {_input.package} {safe_string(_input.version)}"
        )

    def command_type(self) -> CommandType:
        return CommandType.sdkman


class CommandUnZipConverter(CommandConverter[CommandUnZip]):
    """
    A :class:`CommandConverter` for :class:`CommandUnZip`.
    """

    def convert(self, _input: CommandUnZip) -> Bash:
        source = or_result(_input.source)

        return join_lines(
            [
                f"unzip -o {source} {join(_input.extract)} -d {_input.target}",
            ]
        )

    def command_type(self) -> CommandType:
        return CommandType.unzip


class CommandWgetConverter(CommandConverter[CommandWget]):
    """
    A :class:`CommandConverter` for :class:`CommandWget`.
    """

    def convert(self, _input: CommandWget) -> Bash:
        return sudo(
            _input,
            f"wget {_input.url} -P {_input.target}; result="
        )

    def command_type(self) -> CommandType:
        return CommandType.wget


class CommandModuleConverter(ModuleConverter[CommandModule], ABC):
    """
    Types a :class:`BashConverter` for :class:`CommandModule`.
    """

    def convert_commands(self, _input: CommandModule) -> set[Bash]:
        return set(
            map(
                lambda c: first(self.command_converters, lambda cc: cc.accepts(c)).convert(c),
                _input.commands
            ),
        )

    def convert(self, _input: CommandModule) -> Bash:
        return join_lines(
            self.convert_commands(_input)
        )

    def __init__(
            self,
            command_converters: set[CommandConverter]
    ) -> None:
        super().__init__()

        self.command_converters = command_converters


class DriverModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`DriverModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.driver


class SDKModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`SDKModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.sdk


class ToolModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`ToolModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.tool


class VPNModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`VPNModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.vpn
