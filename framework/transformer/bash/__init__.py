from framework.transformer.bash.command import CommandAPTConverter, CommandBashConverter, CommandCopyConverter, \
    CommandDartPubConverter, CommandGunZipConverter, CommandNPMConverter, CommandRemoveConverter, \
    CommandSDKManConverter, CommandUnZipConverter, DriverModuleConverter, SDKModuleConverter, ToolModuleConverter, \
    VPNModuleConverter
from framework.transformer.bash.configuration import AliasModuleConverter, GitConfigModuleConverter
from framework.transformer.bash.module import ModuleFactory

command_converters = {
    CommandAPTConverter(),
    CommandBashConverter(),
    CommandCopyConverter(),
    CommandDartPubConverter(),
    CommandGunZipConverter(),
    CommandNPMConverter(),
    CommandRemoveConverter(),
    CommandSDKManConverter(),
    CommandUnZipConverter(),
}

bash_module_factory = ModuleFactory(
    {
        AliasModuleConverter(),
        GitConfigModuleConverter(),
        DriverModuleConverter(command_converters),
        SDKModuleConverter(command_converters),
        ToolModuleConverter(command_converters),
        VPNModuleConverter(command_converters),
    }
)
