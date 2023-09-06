from framework.core.func import safe_set
from framework.core.types import EnumElement, ObjectElement
from framework.schema.module import Module, ModuleType, ModuleName, ModuleDependency


class CommandTypeEnum(EnumElement):
    pass


class CommandType(CommandTypeEnum):
    """
    Describes the possible tools that can be used to install packages.
    """
    apt = CommandTypeEnum("apt")
    bash = CommandTypeEnum("bash")
    copy = CommandTypeEnum("cp")
    dart_pub = CommandTypeEnum("pub")
    gunzip = CommandTypeEnum("gunzip")
    npm = CommandTypeEnum("npm")
    rm = CommandTypeEnum("rm")
    sdkman = CommandTypeEnum("sdkman")
    unzip = CommandTypeEnum("unzip")
    pass


class Command(ObjectElement):
    """
    Represents the required information to configure a command that executes on the host machine.

    Attributes:
        type: the command to use.
        export: if the command exports new variables to be exported in local sessions (**PATH** variable).
        export_folder: an optional file path to a folder that contains binaries to export.
    """

    def __init__(self, _type: CommandTypeEnum, export: bool = False, export_folder: str = None) -> None:
        super().__init__()

        self.type = _type
        self.export = export
        self.export_folder = export_folder


class CommandAPT(Command):
    """
    Represents the configuration to install a package using apt.

    Attributes:
        package: the identifier of the package recognized by apt.
        url: if package is not provided, the url of .deb file that install the package.
        repositories: a set of apt repositories that are required to fetch the package.
    """

    def __init__(
            self,
            export: bool = False,
            export_folder: str = None,
            package: str = None,
            url: str = None,
            repositories: set[str] = None
    ) -> None:
        super().__init__(
            CommandType.apt,
            export,
            export_folder
        )

        self.package = package
        self.url = url
        self.repositories = safe_set(repositories)


class CommandBash(Command):
    """
    Represents the configuration to execute a bash script.

    Attributes:
        url: the link to the source of a bash script that describes how to install the package.
        source: if url is not provided, a set of lines that compose the bash script.
    """

    def __init__(
            self,
            export: bool = False,
            export_folder: str = None,
            url: str = None,
            source: set[str] = None
    ) -> None:
        super().__init__(
            CommandType.bash,
            export,
            export_folder
        )

        self.url = url
        self.source = safe_set(source)


class CommandCopy(Command):
    """
    Represents the configuration to copy a file/folder to a target using copy (cp).

    Attributes:
        url: the link to a file that will be downloaded with wget and copied to the target destination.
        target: the target destination where the file will be copied to. Defaults to /usr/local/bin.
    """

    def __init__(
            self,
            url: str,
            target: str = "/usr/local/bin",
            export: bool = False,
            export_folder: str = None,
    ) -> None:
        super().__init__(
            CommandType.copy,
            export,
            export_folder
        )
        self.url = url
        self.target = target


class CommandDartPub(Command):
    """
    Represents the configuration to install a package using Dart Pub.

    Attributes:
        package: the package to install available in Dart Pub global registry.
    """

    def __init__(
            self,
            package: str,
            export: bool = False,
            export_folder: str = None,
    ) -> None:
        super().__init__(
            CommandType.dart_pub,
            export,
            export_folder
        )

        self.package = package


class CommandGunZip(Command):
    """
    Represents the configuration to extract files and folders using gunzip (gz).

    Attributes:
        url: the link to a .gz file which files will be extracted.
    """

    def __init__(
            self,
            url: str,
            export: bool = False,
            export_folder: str = None,
    ) -> None:
        super().__init__(
            CommandType.gunzip,
            export,
            export_folder
        )

        self.url = url


class CommandNPM(Command):
    """
    Represents the configuration to install a package using Node NPM.

    Attributes:
        package: the package to install available in Node NPM global registry.
    """

    def __init__(
            self,
            package: str,
            export: bool = False,
            export_folder: str = None,
    ) -> None:
        super().__init__(
            CommandType.npm,
            export,
            export_folder
        )

        self.package = package


class CommandUnZip(Command):
    """
    Represents the configuration to extract files and folders using unzip (zip).

    Attributes:
        url: the link to a .zip file which files will be extracted.
        extract: a set of files to extract from the zip file. Defaults to every file.
        target: the target destination to copy the extracted files. Defaults to /usr/local.
    """

    def __init__(
            self,
            url: str,
            export: bool = False,
            export_folder: str = None,
            extract: set[str] = None,
            target: str = "/usr/local",
    ) -> None:
        super().__init__(
            CommandType.unzip,
            export,
            export_folder
        )

        self.url = url
        self.extract = safe_set(extract)
        self.target = target


class CommandRemove(Command):
    """
    Represents the configuration to remove a file/folder.

    Attributes:
        target: the target destination to remove. Defaults to /usr/local.
    """

    def __init__(
            self,
            target: str,
            export: bool = False,
            export_folder: str = None,
    ) -> None:
        super().__init__(
            CommandType.rm,
            export,
            export_folder
        )

        self.target = target


class CommandSDKMan(Command):
    """
    Represents the configuration to install a package using SDKMAN.

    Attributes:
        package: the package to install, recognized by SDKMAN.
    """

    def __init__(
            self,
            package: str,
            export: bool = False,
            export_folder: str = None,
    ) -> None:
        super().__init__(
            CommandType.sdkman,
            export,
            export_folder
        )

        self.package = package


class CommandModule(Module):
    """
    Represents a module that instructs how to execute commands.

    Attributes:
        commands: a set of :class:`Command` with instruction on how to execute a command.
    """

    def __init__(
            self,
            commands: set[Command],
            _type: ModuleType,
            name: ModuleName,
            dependencies: set[ModuleDependency] = None
    ) -> None:
        super().__init__(_type, name, dependencies)

        self.commands = commands


class DriverModule(CommandModule):
    """
    Represents a :class:`Module` that instructs how to install a driver.
    """

    def __init__(self, commands: set[Command], name: ModuleName, dependencies: set[ModuleDependency]):
        super().__init__(commands, ModuleType.driver, name, dependencies)


class ToolModule(CommandModule):
    """
    Represents a :class:`Module` that instructs how to install a tool.
    """

    def __init__(self, commands: set[Command], name: ModuleName, dependencies: set[ModuleDependency]):
        super().__init__(commands, ModuleType.tool, name, dependencies)


class SDKModule(CommandModule):
    """
    Represents a :class:`Module` that instructs how to install an SDK.
    """

    def __init__(self, commands: set[Command], name: ModuleName, dependencies: set[ModuleDependency]):
        super().__init__(commands, ModuleType.sdk, name, dependencies)


class VPNModule(CommandModule):
    """
    Represents a :class:`Module` that instructs how to install a VPN.
    """

    def __init__(self, commands: set[Command], name: ModuleName, dependencies: set[ModuleDependency]):
        super().__init__(commands, ModuleType.vpn, name, dependencies)