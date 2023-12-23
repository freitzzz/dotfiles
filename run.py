#!/usr/bin/env python3
import argparse

from framework.core.const import installed_modules_path
from framework.core.log import put_snakes_to_work, ConsoleLumberSnakeClient
from framework.installer.installer import Installer
from framework.transformer.bash import bash_module_factory
from framework.transformer.json import json_module_factory, json_profile_factory

argument_parser = argparse.ArgumentParser(
    description="Configures modules using dotfiles framework",
)

argument_parser.add_argument(
    "-d",
    "--directory",
    help="path to a directory that contains module files to load by the framework",
    default=".",
    required=False
)

argument_parser.add_argument(
    "-p",
    "--profile",
    help="path to a profile file that specifies a set of modules to configure",
    required=False
)

args = argument_parser.parse_args()

put_snakes_to_work(
    [
        ConsoleLumberSnakeClient()
    ]
)

installer = Installer(
    installed_modules_directory=installed_modules_path,
    modules_directory=args.directory,
    profile_path=args.profile,
    _json_module_factory=json_module_factory,
    _bash_module_factory=bash_module_factory,
    _json_profile_factory=json_profile_factory,

)

installer.run()
