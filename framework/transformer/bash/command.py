from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from framework.core.func import first, join_lines
from framework.core.types import Bash
from framework.schema.command import \
    CommandAPT, CommandBash, CommandNPM, \
    CommandCopy, CommandRemove, CommandUnZip, CommandGunZip, CommandDartPub, CommandSDKMan, CommandType
from framework.schema.command import CommandModule, Command
from framework.schema.module import ModuleType
from framework.transformer.bash.module import ModuleConverter
from framework.transformer.bash.transformer import BashConverter

C = TypeVar('C', Command, Command)


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
        if len(_input.source) > 0:
            return join_lines(_input.source)

        return f"wget -qO- {_input.url} | bash"

    def command_type(self) -> CommandType:
        return CommandType.bash


class CommandCopyConverter(CommandConverter[CommandCopy]):
    """
    A :class:`CommandConverter` for :class:`CommandCopy`.
    """

    def convert(self, _input: CommandCopy) -> Bash:
        return f"wget {_input.url} -O {_input.target}"

    def command_type(self) -> CommandType:
        return CommandType.copy


class CommandDartPubConverter(CommandConverter[CommandDartPub]):
    """
    A :class:`CommandConverter` for :class:`CommandDartPub`.
    """

    def convert(self, _input: CommandDartPub) -> Bash:
        return f"dart pub global activate {_input.package}"

    def command_type(self) -> CommandType:
        return CommandType.dart_pub


class CommandGunZipConverter(CommandConverter[CommandGunZip]):
    """
    A :class:`CommandConverter` for :class:`CommandGunZip`.
    """

    def convert(self, _input: CommandGunZip) -> Bash:
        url_hash = hash(_input.url)

        temp_gz_fp = f"/tmp/{url_hash}.gz"
        temp_tar_fp = f"/tmp/{url_hash}.tar"

        return join_lines(
            [
                f"wget {_input.url} -O {temp_gz_fp}",
                f"gunzip {temp_gz_fp}",
                f"tar -xf {temp_tar_fp} -C {_input.export_folder}",
            ]
        )

    def command_type(self) -> CommandType:
        return CommandType.gunzip


class CommandNPMConverter(CommandConverter[CommandNPM]):
    """
    A :class:`CommandConverter` for :class:`CommandNPM`.
    """

    def convert(self, _input: CommandNPM) -> Bash:
        return f"sudo npm install -g {_input.package}"

    def command_type(self) -> CommandType:
        return CommandType.npm


class CommandRemoveConverter(CommandConverter[CommandRemove]):
    """
    A :class:`CommandConverter` for :class:`CommandRemove`.
    """

    def convert(self, _input: CommandRemove) -> Bash:
        return f"rm -rf {_input.target}"

    def command_type(self) -> CommandType:
        return CommandType.rm


class CommandSDKManConverter(CommandConverter[CommandSDKMan]):
    """
    A :class:`CommandConverter` for :class:`CommandSDKMan`.
    """

    def convert(self, _input: CommandSDKMan) -> Bash:
        return f"sdk install {_input.package} {_input.package} <version>"

    def command_type(self) -> CommandType:
        return CommandType.sdkman


class CommandUnZipConverter(CommandConverter[CommandUnZip]):
    """
    A :class:`CommandConverter` for :class:`CommandUnZip`.
    """

    def convert(self, _input: CommandUnZip) -> Bash:
        url_hash = hash(_input.url)

        temp_zip_fp = f"/tmp/{url_hash}.zip"

        return join_lines(
            [
                f"wget {_input.url} -O {temp_zip_fp}",
                f"unzip -o {temp_zip_fp} -d {_input.export_folder}",
            ]
        )

    def command_type(self) -> CommandType:
        return CommandType.unzip


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
