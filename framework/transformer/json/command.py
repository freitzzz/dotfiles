from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from framework.core.func import first
from framework.core.types import JSON
from framework.schema.command import \
    CommandAPT, CommandType, CommandBash, CommandNPM, \
    CommandCopy, CommandRemove, CommandUnZip, CommandGunZip, CommandDartPub, CommandSDKMan, CommandWget, CommandTar
from framework.schema.command import CommandModule, VPNModule, DriverModule, ToolModule, SDKModule, Command
from framework.schema.module import ModuleType, ModuleName
from framework.transformer.json.module import ModuleConverter, ModuleDependencyConverter
from framework.transformer.json.transformer import JsonConverter

C = TypeVar('C', bound=Command)


class CommandConverter(JsonConverter[C], Generic[C]):
    """
    Types a :class:`JsonConverter` for :class:`Command`.
    """

    def accepts(self, _input: JSON) -> bool:
        return _input.get('type') == self.command_type().value

    @abstractmethod
    def command_type(self) -> CommandType:
        """
        Describes the command to convert type.

        :return: the :class:`CommandType` that describes this converter.
        """
        ...


class CommandAPTConverter(CommandConverter[CommandAPT]):
    """
    A :class:`CommandConverter` for :class:`CommandAPT`.
    """

    def command_type(self) -> CommandType:
        return CommandType.apt

    def convert(self, _input: JSON) -> CommandAPT:
        return CommandAPT(
            package=_input.get('package'),
            url=_input.get('url'),
            repositories=_input.get('repositories'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandBashConverter(CommandConverter[CommandBash]):
    """
    A :class:`CommandConverter` for :class:`CommandBash`.
    """

    def command_type(self) -> CommandType:
        return CommandType.bash

    def convert(self, _input: JSON) -> CommandBash:
        return CommandBash(
            url=_input.get('url'),
            source=_input.get('source'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandCopyConverter(CommandConverter[CommandCopy]):
    """
    A :class:`CommandConverter` for :class:`CommandCopy`.
    """

    def command_type(self) -> CommandType:
        return CommandType.copy

    def convert(self, _input: JSON) -> CommandCopy:
        return CommandCopy(
            source=_input.get('source'),
            target=_input.get('target'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandDartPubConverter(CommandConverter[CommandDartPub]):
    """
    A :class:`CommandConverter` for :class:`CommandDartPub`.
    """

    def command_type(self) -> CommandType:
        return CommandType.dart_pub

    def convert(self, _input: JSON) -> CommandDartPub:
        return CommandDartPub(
            package=_input.get('package'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandGunZipConverter(CommandConverter[CommandGunZip]):
    """
    A :class:`CommandConverter` for :class:`CommandGunZip`.
    """

    def command_type(self) -> CommandType:
        return CommandType.gunzip

    def convert(self, _input: JSON) -> CommandGunZip:
        return CommandGunZip(
            source=_input.get('source'),
            target=_input.get('target'),
            tar=_input.get('tar'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandNPMConverter(CommandConverter[CommandNPM]):
    """
    A :class:`CommandConverter` for :class:`CommandNPM`.
    """

    def command_type(self) -> CommandType:
        return CommandType.npm

    def convert(self, _input: JSON) -> CommandNPM:
        return CommandNPM(
            package=_input.get('package'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandRemoveConverter(CommandConverter[CommandRemove]):
    """
    A :class:`CommandConverter` for :class:`CommandRemove`.
    """

    def command_type(self) -> CommandType:
        return CommandType.rm

    def convert(self, _input: JSON) -> CommandRemove:
        return CommandRemove(
            target=_input.get('target'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandSDKManConverter(CommandConverter[CommandSDKMan]):
    """
    A :class:`CommandConverter` for :class:`CommandSDKMan`.
    """

    def command_type(self) -> CommandType:
        return CommandType.sdkman

    def convert(self, _input: JSON) -> CommandSDKMan:
        return CommandSDKMan(
            package=_input.get('package'),
            version=_input.get('version'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandTarConverter(CommandConverter[CommandTar]):
    """
    A :class:`CommandConverter` for :class:`CommandTar`.
    """

    def command_type(self) -> CommandType:
        return CommandType.tar

    def convert(self, _input: JSON) -> CommandTar:
        return CommandTar(
            extract=_input.get('extract'),
            source=_input.get('source'),
            target=_input.get('target'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandUnZipConverter(CommandConverter[CommandUnZip]):
    """
    A :class:`CommandConverter` for :class:`CommandUnZip`.
    """

    def command_type(self) -> CommandType:
        return CommandType.unzip

    def convert(self, _input: JSON) -> CommandUnZip:
        return CommandUnZip(
            extract=_input.get('extract'),
            source=_input.get('source'),
            target=_input.get('target'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandWgetConverter(CommandConverter[CommandWget]):
    """
    A :class:`CommandConverter` for :class:`CommandWget`.
    """

    def command_type(self) -> CommandType:
        return CommandType.wget

    def convert(self, _input: JSON) -> CommandWget:
        return CommandWget(
            url=_input.get('url'),
            target=_input.get('target'),
            sudo=_input.get('sudo'),
            export=_input.get('export'),
            export_folder=_input.get('export_folder'),
        )


class CommandModuleConverter(ModuleConverter[CommandModule], ABC):
    """
    Types a :class:`JsonConverter` for :class:`CommandModule`.
    """

    def accepts(self, _input: JSON) -> bool:
        return super().accepts(_input) and _input.get('commands') is not None

    def convert_commands(self, _input: JSON) -> set[Command]:
        return set(
            map(
                lambda c: first(self.command_converters, lambda cc: cc.accepts(c)).convert(c),
                _input.get('commands', [])
            ),
        )

    def __init__(
            self,
            dependency_converter: ModuleDependencyConverter,
            command_converters: set[CommandConverter]
    ) -> None:
        super().__init__(dependency_converter)

        self.command_converters = command_converters


class DriverModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`DriverModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.driver

    def convert(self, _input: JSON) -> DriverModule:
        return DriverModule(
            name=ModuleName(_input.get('name')),
            commands=self.convert_commands(_input),
            dependencies=self.dependency_converter.convert_multiple(
                _input.get('dependencies')
            )
        )

    def __init__(
            self,
            dependency_converter: ModuleDependencyConverter,
            command_converts: set[CommandConverter]
    ) -> None:
        super().__init__(dependency_converter, command_converts)


class SDKModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`SDKModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.sdk

    def convert(self, _input: JSON) -> SDKModule:
        return SDKModule(
            name=ModuleName(_input.get('name')),
            commands=self.convert_commands(_input),
            dependencies=self.dependency_converter.convert_multiple(
                _input.get('dependencies')
            )
        )

    def __init__(
            self,
            dependency_converter: ModuleDependencyConverter,
            command_converts: set[CommandConverter]
    ) -> None:
        super().__init__(dependency_converter, command_converts)


class ToolModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`ToolModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.tool

    def convert(self, _input: JSON) -> ToolModule:
        return ToolModule(
            name=ModuleName(_input.get('name')),
            commands=self.convert_commands(_input),
            dependencies=self.dependency_converter.convert_multiple(
                _input.get('dependencies')
            )
        )

    def __init__(
            self,
            dependency_converter: ModuleDependencyConverter,
            command_converts: set[CommandConverter]
    ) -> None:
        super().__init__(dependency_converter, command_converts)


class VPNModuleConverter(CommandModuleConverter):
    """
    A :class:`ModuleConverter` for :class:`VPNModule`.
    """

    def module_type(self) -> ModuleType:
        return ModuleType.vpn

    def convert(self, _input: JSON) -> VPNModule:
        return VPNModule(
            name=ModuleName(_input.get('name')),
            commands=self.convert_commands(_input),
            dependencies=self.dependency_converter.convert_multiple(
                _input.get('dependencies')
            )
        )

    def __init__(
            self,
            dependency_converter: ModuleDependencyConverter,
            command_converts: set[CommandConverter]
    ) -> None:
        super().__init__(dependency_converter, command_converts)
