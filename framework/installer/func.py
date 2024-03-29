import json
import os
from tempfile import mktemp
from typing import Iterable

from framework.core.const import configuration_directory_path, dotfiles_init_path, user_session_environment_path, \
    exported_paths_path
from framework.core.func import join_lines, join
from framework.core.types import StringElement, MapElement, ObjectElement, Element, Bash, JSON, Factory
from framework.schema.module import Module
from framework.schema.profile import Profile


def write_file(file_path: str, content: str | Iterable[str], mode="w") -> None:
    """
    Allows writing content to a specific file using Python builtins.

    :param file_path: path that locates the file in the filesystem.
    :param content: the content to write in the file, as a string (plaintext) or list of strings (lines)
    :param mode: the file read/write mode. defaults to "w" (truncate + write)
    """

    with(open(file_path, mode) as file):
        file.write(content if isinstance(content, str) else join_lines(content))
        file.close()


def remove_duplicate_file(file_path: str) -> None:
    """
    Removes duplicate lines of a specific file using Python builtins.

    :param file_path: path that locates the file in the filesystem.
    """

    lines = open(file_path, 'r').readlines()
    lines_without_duplicates = list(dict.fromkeys(lines))
    open(file_path, 'w').write(join(lines_without_duplicates, ''))


def element_to_primitive(element: Element) -> object:
    """
    Converts the structure of an element in a primitive representation (string, int, float, object, dict, list, bool).

    :param element: the element to convert in a primitive object.
    :return: the converted primitive.
    """

    if isinstance(element, StringElement | MapElement):
        return element.value
    elif isinstance(element, set | list):
        return list(map(lambda x: element_to_primitive(x), element))
    elif isinstance(element, ObjectElement):
        entries = map(lambda x: (x[0], element_to_primitive(x[1])), element.__dict__.items())
        return dict(filter(lambda x: x[0] != '_type', entries))
    else:
        return element


def eval_bash(script: Bash) -> int:
    """
    Evaluates a bash script.

    :param script: the bash script to execute.
    :return: a POSIX status code on whether the script executed with any errors.
    """

    temp_file = mktemp()

    write_file(
        temp_file,
        content=[
            "set -e",
            "source ~/.profile",
            script
        ],
        mode="x"
    )

    return os.system(f"cd /tmp; bash {temp_file}")


def load_modules(
        json_module_factory: Factory[JSON, Module],
        directory: str
) -> set[Module]:
    """
    Loads all modules at a given directory, by scanning through modules JSON.

    :param json_module_factory: the factory instance to use for converting JSON to :class:`Module`.
    :param directory: the directory location to scan modules.
    :return: a set of :class:`Module` found in the requested directory.
    """

    return json_module_factory.create_multiple(
        __find_modules_json__(directory)
    )


def save_modules(
        modules_directory: str,
        modules: set[Module],
) -> None:
    """
    Saves a set modules at a given directory.

    :param modules_directory: the directory location to save modules.
    :param modules: the set of modules to save.
    """

    if not os.path.exists(modules_directory):
        os.mkdir(modules_directory)

    modules_types = set(map(lambda x: x.type, modules))

    for module_type in modules_types:
        module_directory_path = f"{modules_directory}/{module_type}"

        if not os.path.exists(module_directory_path):
            os.mkdir(module_directory_path)

    for module in modules:
        module_directory_path = f"{modules_directory}/{module.type}"
        module_file_path = f"{module_directory_path}/{module.name}.json"

        if not os.path.exists(module_file_path):
            write_file(module_file_path, json.dumps(element_to_primitive(module)))


def load_profile(
        json_profile_factory: Factory[JSON, Profile],
        path: str,
) -> Profile:
    """
    Loads the profile at a given file path.

    :param json_profile_factory: the factory instance to use for converting JSON to :class:`Profile`.
    :param path: the file location to load profile configuration.
    :return: an instance of :class:`Profile` based on the file path provided.
    """

    return json_profile_factory.create(
        json.load(open(path))
    )


def init_internals() -> None:
    """
    Initializes the internal files created and used by the framework.
    """

    if not os.path.exists(configuration_directory_path):
        os.mkdir(configuration_directory_path)
        write_file(exported_paths_path, [])

    if not os.path.exists(dotfiles_init_path):
        write_file(
            dotfiles_init_path,
            content=[
                "# THIS FILE IS AUTOMATICALLY UPDATED BY THE FRAMEWORK. DO NOT DELETE",
                f"source {exported_paths_path}",
            ]
        )

        write_file(
            user_session_environment_path,
            content=[
                "# Generated by dotfiles framework. DO NOT DELETE",
                f"source {dotfiles_init_path}",
                "# https://github.com/freitzzz/dotfiles/",
            ],
            mode="a"
        )


def clean_internals() -> None:
    """
    Cleans (removes duplicate lines) the internal files created and used by the framework.
    """

    remove_duplicate_file(exported_paths_path)
    remove_duplicate_file(dotfiles_init_path)


def __find_modules_json__(modules_directory: str) -> list[JSON]:
    """
    Finds all modules at a given directory, mapping the found models in JSON.

    :param modules_directory: the path to a directory to scan modules.
    :return: a list modules represented in JSON.
    """

    _modules: list[JSON] = []

    for current_path, _, files in os.walk(modules_directory):
        for file in files:
            if file.endswith('.json'):
                _json = json.load(open(os.path.join(current_path, file)))
                if _json.get('definitions') is None:
                    _modules.append(_json)

    return _modules
