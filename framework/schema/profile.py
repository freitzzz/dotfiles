from framework.core.func import safe_set
from framework.core.types import StringElement, ObjectElement
from framework.schema.module import ModuleDependency

ModuleDefinition = ModuleDependency


class ProfileIdentifier(StringElement):
    """
    Describes the profile name.
    """

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self):
        return self.value

    pass


class Profile(ObjectElement):
    """
    Represents a profile that targets a user/environment/device. A module defines what modules the target requires to
    configure on the machine.

    Attributes:
        name: the profile name.
        modules: a set of module definitions that will be loaded for configuration in the device.
    """

    def __init__(
            self,
            name: ProfileIdentifier,
            modules: set[ModuleDefinition] = None
    ) -> None:
        super().__init__()

        self.name = name
        self.modules = safe_set(modules)

    @staticmethod
    def default(modules: set[ModuleDefinition]):
        """
        Creates a default profile.

        :param modules: the set of default modules to load.
        :return: the default profile instance.
        """
        return Profile(
            ProfileIdentifier("default"),
            modules
        )

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __str__(self):
        return f"Profile({self.name})"
