from framework.core.func import first
from framework.core.log import log_info, log_error, log_warning
from framework.installer.func import init_internals, eval_bash, \
    load_modules, save_modules
from framework.schema.module import Module
from framework.transformer.bash import ModuleFactory as BashModuleFactory
from framework.transformer.json import ModuleFactory as JsonModuleFactory


class Installer:
    def __init__(
            self,
            installed_modules_directory: str,
            modules_directory: str,
            _json_module_factory: JsonModuleFactory,
            _bash_module_factory: BashModuleFactory
    ):
        self.installed_modules_directory = installed_modules_directory
        self.modules_directory = modules_directory
        self.json_module_factory = _json_module_factory
        self.bash_module_factory = _bash_module_factory

        self.installed_modules = load_modules(self.json_module_factory, self.installed_modules_directory)
        self.modules_to_install = load_modules(self.json_module_factory, self.modules_directory)

        init_internals()

    def run(self):
        abc = self.modules_to_install.difference(self.installed_modules)

        if len(abc) == 0:
            log_info("All modules are already installed.")
            return

        for module in abc:
            try:
                log_info(f"installing {module}")
                self._install_module(module)
            except BaseException as exception:
                log_error("something went wrong during module installation.", exception)

        save_modules(
            self.installed_modules_directory,
            self.installed_modules,
        )

    def _install_module(self, module: Module):
        if module in self.installed_modules:
            log_info(f"Module {module} already installed, skipping")
            return

        self._install_dependencies(module)

        bash_script = self.bash_module_factory.create(module)
        _exit_code = eval_bash(bash_script)

        if _exit_code == 0:
            log_info(f"installed {module}")
            self.installed_modules.add(module)
        else:
            log_warning(f"failed to install {module}")

    def _install_dependencies(self, module: Module):
        module_dependencies = self._module_dependencies(module)

        for module_dependency in module_dependencies:
            log_info(f"installing dependency {module_dependency} of module {module}")
            self._install_module(module_dependency)

    def _module_dependencies(self, module: Module) -> set[Module]:
        required_dependencies = set[module]()

        for dependency in module.dependencies:
            module_dependency_match = first(
                self.modules_to_install,
                lambda m: m.type == dependency.type and m.name == dependency.name,
                lambda: None
            )

            if module_dependency_match is None:
                raise Exception(f"no module matching dependency {dependency} was found.")

            required_dependencies.add(module_dependency_match)

        return required_dependencies.difference(self.installed_modules)