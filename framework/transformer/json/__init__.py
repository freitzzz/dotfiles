from framework.transformer.json.command import CommandAPTConverter, CommandBashConverter, CommandCopyConverter, \
    CommandDartPubConverter, CommandGunZipConverter, CommandNPMConverter, CommandRemoveConverter, \
    CommandSDKManConverter, CommandUnZipConverter, DriverModuleConverter, SDKModuleConverter, ToolModuleConverter, \
    VPNModuleConverter, CommandWgetConverter, CommandTarConverter
from framework.transformer.json.configuration import AliasModuleConverter, GitConfigModuleConverter
from framework.transformer.json.module import ModuleDependencyConverter, ModuleFactory
from framework.transformer.json.profile import ProfileFactory, ProfileConverter

command_converters = {
    CommandAPTConverter(),
    CommandBashConverter(),
    CommandCopyConverter(),
    CommandDartPubConverter(),
    CommandGunZipConverter(),
    CommandNPMConverter(),
    CommandRemoveConverter(),
    CommandSDKManConverter(),
    CommandTarConverter(),
    CommandUnZipConverter(),
    CommandWgetConverter()
}

dependency_converter = ModuleDependencyConverter()

json_module_factory = ModuleFactory(
    {
        AliasModuleConverter(dependency_converter),
        GitConfigModuleConverter(dependency_converter),
        DriverModuleConverter(dependency_converter, command_converters),
        SDKModuleConverter(dependency_converter, command_converters),
        ToolModuleConverter(dependency_converter, command_converters),
        VPNModuleConverter(dependency_converter, command_converters),
    }
)

json_profile_factory = ProfileFactory(
    {
        ProfileConverter(dependency_converter)
    }
)
