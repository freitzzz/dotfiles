#!/usr/bin/env python3

import json
import os

from framework.core.types import JSON, Factory, Bash
from framework.schema.module import Module
from framework.transformer.bash import bash_module_factory
from framework.transformer.json import json_module_factory


def find_modules(modules_directory: str) -> list[JSON]:
    _modules = []

    for current_path, folders, files in os.walk(modules_directory):
        for file in files:
            if file.endswith('.json'):
                _json = json.load(open(os.path.join(current_path, file)))
                if _json.get('definitions') is None:  # is None and (_json.get('type') == 'tool'):
                    _modules.append(_json)

    return _modules


class Installer:
    def __init__(
            self,
            configuration_directory: str,
            modules_directory: str,
            _json_module_factory: Factory[JSON, Module],
            _bash_module_factory: Factory[Module, Bash]
    ):
        self.configuration_directory = configuration_directory
        self.modules_directory = modules_directory
        self.json_module_factory = _json_module_factory
        self.bash_module_factory = _bash_module_factory

        self.installed_modules = self._load_installed_modules()
        self.modules_to_install = self._load_modules_to_install()

    def run(self):
        modules_to_install = self.modules_to_install.difference(self.modules_to_install)

        for module in modules_to_install:
            print(f"installing {module}")
            self._install_module(module)

        self._save_installed_modules()

    def _install_module(self, module: Module):
        if module in self.installed_modules:
            pass

        self._install_dependencies(module)

        bash_script = self.bash_module_factory.create(module)
        _exit_code = os.system(f'eval "{bash_script}"')

        if _exit_code == 0:
            print(f"installed {module}")
            self.installed_modules.append(module)
        else:
            print(f"failed to install {module}")

    def _install_dependencies(self, module: Module):
        module_dependencies = self._module_dependencies(module)

        for module_dependency in module_dependencies:
            print(f"installing {module_dependency} dependency of module {module}")
            self._install_module(module_dependency)

    def _module_dependencies(self, module: Module) -> set[Module]:
        required_dependencies = set[module](
            filter(
                lambda d: len(
                    list(
                        filter(
                            lambda m: m.type == d.type and m.name == d.name, self.modules_to_install
                        )
                    )
                ) > 0, module.dependencies
            )
        )

        return required_dependencies.difference(self.installed_modules)

    def _load_installed_modules(self):
        return self.json_module_factory.create_multiple(
            find_modules(self.configuration_directory)
        )

    def _load_modules_to_install(self):
        return self.json_module_factory.create_multiple(
            find_modules(self.modules_directory)
        )

    def _save_installed_modules(self):
        for module in self.installed_modules:
            module_file_path = f"{self.configuration_directory}/{module.name}_{module.type}.json"

            with(open(module_file_path, "w")) as file:
                file.write(json.dumps(module))
                file.close()


installer = Installer(
    "~/.dotfiles",
    ".aliases",
    json_module_factory,
    bash_module_factory,
)

installer.run()

#
# modules = find_modules()
#
# modules = json_module_factory.create_multiple(modules)
# modules = list(
#     filter(
#         lambda m: isinstance(m, CommandModule) and len(
#             list(filter(lambda cm: isinstance(cm, CommandWget), m.commands))
#         ),
#         modules
#     )
# )
#
# print(len(modules))
#
# scripts = bash_module_factory.create_multiple(modules)
#
# for script in scripts:
#     # print(script)
#     # continue
#     temp = mktemp()
#
#     file = open(temp, "w+")
#     file.write(script)
#     file.close()
#
#     exit_code = os.system(f"cat {temp} | bash")
#
#     print(f"=>>>>>>> {exit_code} | {script}")
