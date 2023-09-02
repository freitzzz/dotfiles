#!/usr/bin/env python3

import os
import json

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
    exportFolder: str

    def __init__(
        self,
        type: InstallationToolType,
        export: bool = False,
        exportFolder: str = None
    ) -> None:
        self.type = type
        self.export = export
        self.exportFolder = exportFolder


class InstallCommandAPT(InstallCommand):
    package: str
    url: str
    repositories: set[str]

    def __init__(
        self,
        export: bool = False,
        exportFolder: str = None,
        package: str = None,
        url: str = None,
        repositories: str = []
    ) -> None:
        super().__init__(
            InstallationToolType("apt"),
            export,
            exportFolder
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
        exportFolder: str = None,
        url: str = None,
        source: str = []
    ) -> None:
        super().__init__(
            InstallationToolType("bash"),
            export,
            exportFolder
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
        exportFolder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("cp"),
            export,
            exportFolder
        )
        self.url = url
        self.target = target


class InstallCommandDartPub(InstallCommand):
    package: str

    def __init__(
        self,
        package: str,
        export: bool = False,
        exportFolder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("pub"),
            export,
            exportFolder
        )

        self.package = package


class InstallCommandGunZip(InstallCommand):
    url: str

    def __init__(
        self,
        url: str,
        export: bool = False,
        exportFolder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("gz"),
            export,
            exportFolder
        )

        self.url = url


class InstallCommandNPM(InstallCommand):
    package: str

    def __init__(
        self,
        package: str,
        export: bool = False,
        exportFolder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("npm"),
            export,
            exportFolder
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
        exportFolder: str = None,
        extract: str = [],
        target: str = "/usr/local",
    ) -> None:
        super().__init__(
            InstallationToolType("unzip"),
            export,
            exportFolder
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
        exportFolder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("rm"),
            export,
            exportFolder
        )

        self.target = target


class InstallCommandSDKMan(InstallCommand):
    package: str

    def __init__(
        self,
        package: str,
        export: bool = False,
        exportFolder: str = None,
    ) -> None:
        super().__init__(
            InstallationToolType("apt"),
            export,
            exportFolder
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
