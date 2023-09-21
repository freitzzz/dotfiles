from framework.core.func import safe_set
from framework.core.types import EnumElement, StringElement, ObjectElement


class ModuleName(StringElement):
    """
    Describes the module name.
    """

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self):
        return self.value

    pass


class ModuleTypeEnum(EnumElement):

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self):
        return self.value

    pass


class ModuleType(StringElement):
    """
    Describes the type of module.
    """
    alias = ModuleTypeEnum("alias")
    driver = ModuleTypeEnum("driver")
    git_config = ModuleTypeEnum("git-config")
    sdk = ModuleTypeEnum("sdk")
    tool = ModuleTypeEnum("tool")
    vpn = ModuleTypeEnum("vpn")
    pass


class ModuleDependency(ObjectElement):
    """
    Describes a module dependency.

    Attributes:
        type: dependency module type.
        name: dependency module name.
    """

    def __init__(self, _type: ModuleType, name: ModuleName) -> None:
        super().__init__()

        self.type = _type
        self.name = name

    def __hash__(self):
        return hash(self.name) + hash(self.type)

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __str__(self):
        return f"{self.type}({self.name})"


class Module(ObjectElement):
    """
    Represents a module base configuration. A module is a small, composable unit, that instructs how to
    execute a set of operations on the host machine.

    Attributes:
        type: the module type.
        name: the module name.
        dependencies: a set of module dependencies that are required to interpret this module.
    """

    def __init__(
            self,
            _type: ModuleType,
            name: ModuleName,
            dependencies: set[ModuleDependency] = None
    ) -> None:
        super().__init__()

        self.type = _type
        self.name = name
        self.dependencies = safe_set(dependencies)

    def __hash__(self):
        return hash(self.name) & hash(self.type)

    def __eq__(self, other):
        # print(f"wtf: {self} == {other} ({self.__hash__() == hash(other)})")
        return self.__hash__() == hash(other)

    def __str__(self):
        return f"{self.type}({self.name})"
