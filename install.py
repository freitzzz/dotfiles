#!/usr/bin/env python3

import os
import json

from abc import abstractmethod

from typing import Generic, TypeVar, Any

JSON = dict[str, Any]


def extract_commands(json: JSON) -> list[JSON]:
    commands = json.get('command', json.get('commands'))

    return commands if isinstance(commands, list) else [commands]


module_types = [
    "alias",
    "driver",
    "git-config",
    "sdk",
    "tool",
    "vpn"
]

tool_types = [
    "apt",
    "bash",
    "cp",
    "pub",
    "gunzip",
    "npm",
    "unzip",
    "rm",
    "sdkman"
]


def find_modules():
    modules = []

    for currentpath, folders, files in os.walk('.'):
        for file in files:
            if (file.endswith('.json')):
                modules.append(
                    json.load(open(os.path.join(currentpath, file))))
    return modules


# modules = find_modules()

# print(json.dumps(
#     list(filter(lambda x: x['type'] == 'alias', modules)), indent=2))


class Element:
    _type: type


class ObjectElement(Element):
    _type = object


class MapElement(ObjectElement):
    _inner: dict

    def __init__(self, entries: dict) -> None:
        self._inner = entries


class StringElement(Element):
    value: str

    def __init__(self, value: str) -> None:
        self._type = str
        self.value = value


class EnumElement(StringElement):
    values: set[str]

    def __init__(self, value: str, values: set[str]) -> None:
        super().__init__(value)
        self.values = values


class ModuleName(StringElement):
    pass


class ModuleType(EnumElement):
    def __init__(self, value: str) -> None:
        super().__init__(value, module_types)


class ModuleDependency(ObjectElement):
    type: ModuleType
    name: ModuleName

    def __init__(self, type: ModuleType, name: ModuleName) -> None:
        self.type = type
        self.name = name


class InstallationToolType(EnumElement):
    def __init__(self, value: str) -> None:
        super().__init__(value, tool_types)


class InstallCommand(ObjectElement):
    type: InstallationToolType
    export: bool
    export_folder: str

    def __init__(
        self,
        type: InstallationToolType,
        export: bool = False,
        export_folder: str = None
    ) -> None:
        self.type = type
        self.export = export
        self.export_folder = export_folder


class InstallCommandAPT(InstallCommand):
    package: str
    url: str
    repositories: set[str]

    def __init__(
        self,
        export: bool = False,
        export_folder: str = None,
        package: str = None,
        url: str = None,
        repositories: str = []
    ) -> None:
        super().__init__(
            InstallationToolType("apt"),
            export,
            export_folder
        )

        self.package = package
        self.url = url
        self.repositories = repositories


class InstallCommandBash(InstallCommand):
    url: str
    source: set[str]

    def __init__(
        self,
        export: bool = False,
        export_folder: str = None,
        url: str = None,
        source: str = []
    ) -> None:
        super().__init__(
            InstallationToolType("bash"),
            export,
            export_folder
        )

        self.url = url
        self.source = source


class InstallCommandCopy(InstallCommand):
    url: str
    target: str

    def __init__(
        self,
        url: str,
        target: str,
        export: bool = False,
        export_folder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("cp"),
            export,
            export_folder
        )
        self.url = url
        self.target = target


class InstallCommandDartPub(InstallCommand):
    package: str

    def __init__(
        self,
        package: str,
        export: bool = False,
        export_folder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("pub"),
            export,
            export_folder
        )

        self.package = package


class InstallCommandGunZip(InstallCommand):
    url: str

    def __init__(
        self,
        url: str,
        export: bool = False,
        export_folder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("gz"),
            export,
            export_folder
        )

        self.url = url


class InstallCommandNPM(InstallCommand):
    package: str

    def __init__(
        self,
        package: str,
        export: bool = False,
        export_folder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("npm"),
            export,
            export_folder
        )

        self.package = package


class InstallCommandUnZip(InstallCommand):
    url: str
    extract: set[str]
    target: str

    def __init__(
        self,
        url: str,
        export: bool = False,
        export_folder: str = None,
        extract: str = [],
        target: str = "/usr/local",
    ) -> None:
        super().__init__(
            InstallationToolType("unzip"),
            export,
            export_folder
        )

        self.url = url
        self.extract = extract
        self.target = target


class InstallCommandRemove(InstallCommand):
    target: str

    def __init__(
        self,
        target: str,
        export: bool = False,
        export_folder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("rm"),
            export,
            export_folder
        )

        self.target = target


class InstallCommandSDKMan(InstallCommand):
    package: str

    def __init__(
        self,
        package: str,
        export: bool = False,
        export_folder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("apt"),
            export,
            export_folder
        )

        self.package = package


class AliasEntries(MapElement):
    pass


class GitConfig(MapElement):
    pass


class Module:
    type: ModuleType
    name: ModuleName
    dependencies: set[ModuleType]

    def __init__(
        self,
        type: ModuleType,
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        self.type = type
        self.name = name
        self.dependencies = dependencies


class EntriesModule(Module):
    entries: MapElement

    def __init__(
        self,
        entries: MapElement,
        type: ModuleType,
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            type,
            name,
            dependencies,
        )

        self.entries = entries


class CommandModule(Module):
    commands: set[InstallCommand]

    def __init__(
        self,
        commands: set[InstallCommand],
        type: ModuleType,
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            type,
            name,
            dependencies,
        )

        self.commands = commands


class AliasModule(EntriesModule):
    def __init__(
        self,
        entries: AliasEntries,
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            entries,
            ModuleType("alias"),
            name,
            dependencies,
        )


class GitConfigModule(EntriesModule):
    def __init__(
        self,
        entries: GitConfig,
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            entries,
            ModuleType("git-config"),
            name,
            dependencies,
        )


class DriverModule(CommandModule):
    def __init__(
        self,
        commands: set[InstallCommand],
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            commands,
            ModuleType("driver"),
            name,
            dependencies,
        )


class SDKModule(CommandModule):
    def __init__(
        self,
        commands: set[InstallCommand],
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            commands,
            ModuleType("sdk"),
            name,
            dependencies,
        )


class ToolModule(CommandModule):
    def __init__(
        self,
        commands: set[InstallCommand],
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            commands,
            ModuleType("tool"),
            name,
            dependencies,
        )


class VPNModule(CommandModule):
    def __init__(
        self,
        commands: set[InstallCommand],
        name: ModuleName,
        dependencies: set[ModuleDependency] = []
    ) -> None:
        super().__init__(
            commands,
            ModuleType("vpn"),
            name,
            dependencies,
        )


I = TypeVar('I')
O = TypeVar('O')
M = TypeVar('M', bound=Module)
IC = TypeVar('IC', bound=InstallCommand)


class Converter(Generic[I, O]):

    @abstractmethod
    def accepts(self, input: I) -> bool:
        ...

    @abstractmethod
    def convert(self, input: I) -> O:
        ...


class Factory(Generic[I, O]):
    converters: set[Converter[I, O]]

    def convert(self, input: I):
        ...


class JsonConverter(Converter[JSON, O], Generic[O]):

    @abstractmethod
    def accepts(self, input: JSON) -> bool:
        ...

    @abstractmethod
    def convert(self, input: JSON) -> O:
        ...


class ModuleDependencyConverter(JsonConverter[ModuleDependency]):
    def accepts(self, input: JSON) -> bool:
        return True

    def convert(self, input: JSON) -> ModuleDependency:
        return ModuleDependency(
            name=ModuleName(input.get('name')),
            type=ModuleType(input.get('type'))
        )

    def convert_multiple(self, input: list[JSON]):
        return list(map(lambda json: self.convert(json), input))


class InstallCommandConverter(JsonConverter[IC], Generic[IC]):
    @abstractmethod
    def accepts(self, input: JSON) -> bool:
        return True

    @abstractmethod
    def convert(self, input: JSON) -> IC:
        ...

    def convert_multiple(self, input: list[JSON]) -> set[IC]:
        return list(map(lambda json: self.convert(json), input))


class InstallCommandAPTConverter(InstallCommandConverter[InstallCommandAPT]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'apt'

    def convert(self, input: JSON) -> InstallCommandAPT:
        return InstallCommandAPT(
            package=input.get('package'),
            url=input.get('url'),
            repositories=input.get('repositories', []),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandBashConverter(InstallCommandConverter[InstallCommandBash]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'bash'

    def convert(self, input: JSON) -> InstallCommandBash:
        return InstallCommandBash(
            url=input.get('url'),
            source=input.get('source', []),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandCopyConverter(InstallCommandConverter[InstallCommandCopy]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'cp'

    def convert(self, input: JSON) -> InstallCommandCopy:
        return InstallCommandCopy(
            url=input.get('url'),
            target=input.get('target'),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandDartPubConverter(InstallCommandConverter[InstallCommandDartPub]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'pub'

    def convert(self, input: JSON) -> InstallCommandDartPub:
        return InstallCommandDartPub(
            package=input.get('package'),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandGunZipConverter(InstallCommandConverter[InstallCommandGunZip]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'gunzip'

    def convert(self, input: JSON) -> InstallCommandGunZip:
        return InstallCommandGunZip(
            url=input.get('url'),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandNPMConverter(InstallCommandConverter[InstallCommandNPM]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'npm'

    def convert(self, input: JSON) -> InstallCommandNPM:
        return InstallCommandNPM(
            package=input.get('package'),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandRemoveConverter(InstallCommandConverter[InstallCommandRemove]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'rm'

    def convert(self, input: JSON) -> InstallCommandRemove:
        return InstallCommandRemove(
            target=input.get('target'),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandSDKManConverter(InstallCommandConverter[InstallCommandSDKMan]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'sdkman'

    def convert(self, input: JSON) -> InstallCommandSDKMan:
        return InstallCommandSDKMan(
            package=input.get('package'),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class InstallCommandUnZipConverter(InstallCommandConverter[InstallCommandUnZip]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'unzip'

    def convert(self, input: JSON) -> InstallCommandUnZip:
        return InstallCommandUnZip(
            url=input.get('url'),
            target=input.get('target'),
            extract=input.get('extract', []),
            export=input.get('export', False),
            export_folder=input.get('export_folder'),
        )


class ModuleConverter(JsonConverter[M], Generic[M]):
    dependency_converter: ModuleDependencyConverter

    @abstractmethod
    def accepts(self, input: JSON) -> bool:
        ...

    @abstractmethod
    def convert(self, input: JSON) -> M:
        ...

    def __init__(self, dependency_converter: ModuleDependencyConverter) -> None:
        self.dependency_converter = dependency_converter


class CommandModuleConverter(ModuleConverter[CommandModule]):
    command_converters: set[InstallCommandConverter]

    def accepts(self, input: JSON) -> bool:
        return input.get('command') != None or input.get('commands') != None

    @abstractmethod
    def convert(self, input: JSON) -> CommandModule:
        ...

    def convert_commands(self, input: JSON) -> set[InstallCommand]:
        return set(
            map(
                lambda c: next(
                    x for x in self.command_converters if x.accepts(c)).convert(c),
                extract_commands(input)
            ),
        )

    def __init__(
            self,
            dependency_converter: ModuleDependencyConverter,
            command_converts: set[InstallCommandConverter]
    ) -> None:
        super().__init__(dependency_converter)

        self.command_converters = command_converters


class AliasModuleConverter(ModuleConverter[AliasModule]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'alias'

    def convert(self, input: JSON) -> AliasModule:
        return AliasModule(
            name=input.get('name'),
            entries=AliasEntries(input.get('entries')),
            dependencies=self.dependency_converter.convert_multiple(
                input.get('dependencies', [])
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter) -> None:
        super().__init__(dependency_converter)


class GitConfigModuleConverter(ModuleConverter[GitConfigModule]):
    def accepts(self, input: JSON) -> bool:
        return input.get('type') == 'git-config'

    def convert(self, input: JSON) -> GitConfig:
        return GitConfigModule(
            name=input.get('name'),
            entries=GitConfig(input.get('entries')),
            dependencies=self.dependency_converter.convert_multiple(
                input.get('dependencies', [])
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter) -> None:
        super().__init__(dependency_converter)


class DriverModuleConverter(CommandModuleConverter):
    def accepts(self, input: JSON) -> bool:
        return super().accepts(input) and input.get('type') == 'driver'

    def convert(self, input: JSON) -> DriverModule:
        return DriverModule(
            name=input.get('name'),
            commands=self.convert_commands(input),
            dependencies=self.dependency_converter.convert_multiple(
                input.get('dependencies', [])
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter, command_converts: set[InstallCommandConverter]) -> None:
        super().__init__(dependency_converter, command_converts)


class SDKModuleConverter(CommandModuleConverter):
    def accepts(self, input: JSON) -> bool:
        return super().accepts(input) and input.get('type') == 'sdk'

    def convert(self, input: JSON) -> SDKModule:
        return SDKModule(
            name=input.get('name'),
            commands=self.convert_commands(input),
            dependencies=self.dependency_converter.convert_multiple(
                input.get('dependencies', [])
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter, command_converts: set[InstallCommandConverter]) -> None:
        super().__init__(dependency_converter, command_converts)


class ToolModuleConverter(CommandModuleConverter):
    def accepts(self, input: JSON) -> bool:
        return super().accepts(input) and input.get('type') == 'tool'

    def convert(self, input: JSON) -> ToolModule:
        return ToolModule(
            name=input.get('name'),
            commands=self.convert_commands(input),
            dependencies=self.dependency_converter.convert_multiple(
                input.get('dependencies', [])
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter, command_converts: set[InstallCommandConverter]) -> None:
        super().__init__(dependency_converter, command_converts)


class VPNModuleConverter(CommandModuleConverter):
    def accepts(self, input: JSON) -> bool:
        return super().accepts(input) and input.get('type') == 'vpn'

    def convert(self, input: JSON) -> VPNModule:
        return VPNModule(
            name=input.get('name'),
            commands=self.convert_commands(input),
            dependencies=self.dependency_converter.convert_multiple(
                input.get('dependencies', [])
            )
        )

    def __init__(self, dependency_converter: ModuleDependencyConverter, command_converts: set[InstallCommandConverter]) -> None:
        super().__init__(dependency_converter, command_converts)


command_converters = [
    InstallCommandAPTConverter(),
    InstallCommandBashConverter(),
    InstallCommandCopyConverter(),
    InstallCommandDartPubConverter(),
    InstallCommandGunZipConverter(),
    InstallCommandNPMConverter(),
    InstallCommandRemoveConverter(),
    InstallCommandSDKManConverter(),
    InstallCommandUnZipConverter(),
]

dependency_converter = ModuleDependencyConverter()

module_converters = [
    AliasModuleConverter(dependency_converter),
    GitConfigModuleConverter(dependency_converter),
    DriverModuleConverter(dependency_converter, command_converters),
    SDKModuleConverter(dependency_converter, command_converters),
    ToolModuleConverter(dependency_converter, command_converters),
    VPNModuleConverter(dependency_converter, command_converters),
]

modules = find_modules()

for module in modules:
    for converter in module_converters:
        if (converter.accepts(module)):
            print(converter.convert(module))
