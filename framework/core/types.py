# All possible element types
from abc import abstractmethod
from typing import Generic, TypeVar

from framework.core.func import first

ElementType = str | int | float | bool | object | list

# Types a JSON object
JSON = dict[str, ElementType]

# Types a Bash script
Bash = str

# Input Type
TI = TypeVar('TI')

# Output Type
TO = TypeVar('TO')


class Element:
    """
    Types an abstract element of a module. An element can either be a string, number, boolean, object or array.

    Attributes:
        _type: Specifies the type of the element.
    """
    _type: ElementType

    def __init__(self, _type: ElementType):
        self._type = _type


class ObjectElement(Element):
    """
    Types an object :class:`Element`.
    """

    def __init__(self):
        super().__init__(object)


class MapElement(ObjectElement):
    """
    Types a Map :class:`Element`.

    Attributes:
        value: A dictionary that represents the element value.
    """

    def __init__(self, value: JSON) -> None:
        super().__init__()
        self.value = value


class StringElement(Element):
    """
    Types a String :class:`Element`.

    Attributes:
        value: A string that represents the element value.
    """

    def __init__(self, value: str) -> None:
        super().__init__(str)
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.__hash__() == hash(other)


class EnumElement(StringElement):
    """
    Types a Enum :class:`Element`.
    """

    def __init__(self, value: str) -> None:
        super().__init__(value)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self):
        return self.value


class Converter(Generic[TI, TO]):
    """
    Represents the behaviour of a converter.
    A converter accepts input of type :class:`TI` and converts it into output of type :class:`TO`.
    """

    @abstractmethod
    def accepts(self, _input: TI) -> bool:
        """
        Predicate method that describes if this converter accepts a given input.

        :param _input: the input desired to convert.
        :return: boolean true if this converter can convert the input.
        """
        ...

    @abstractmethod
    def convert(self, _input: TI) -> TO:
        """
        Converts an input into an output.

        :param _input: the input desired to convert.
        :return: the converted output.
        """
        ...

    def convert_multiple(self, _input: list[TI]) -> list[TO] | set[TO]:
        """
        Applies the convert function to a list of input :class:`TI`.

        :param _input: the input desired to convert.
        :return: the converted output.
        """
        return list(map(lambda json: self.convert(json), _input or []))


class Factory(Generic[TI, TO]):
    """
    Represents the behaviour of a factory.
    A factory takes a set of converters and uses the first one that accepts the input to convert it.

    Attributes:
        converters: the set of converters that power the factory.
    """

    def __init__(self, converters: set[Converter[TI, TO]]):
        self.converters = converters

    def a(self):
        Opt
        raise Exception("????")

    def create(self, _input: TI) -> TO:
        """
        Creates a value of type :class:`TO` based on an input of type :class:`TI`.

        :param _input: the input to create the output.
        :return: the output created using the input.
        """
        a = first(self.converters, lambda c: c.accepts(_input), or_else=None)
        print(a)
        print(dict(a))
        return a.convert(_input)

    def create_multiple(self, _input: list[TI]) -> set[TO]:
        """
        Applies the create function to a list of input :class:`TI`.

        :param _input: the input desired to create.
        :return: the created output.
        """
        return set(map(lambda json: self.create(json), _input))
