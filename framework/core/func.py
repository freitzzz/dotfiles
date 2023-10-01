from typing import TypeVar, Callable, Iterable

X = TypeVar('X')
Y = TypeVar('Y')


def first(iterable: set[X] | list[X], where: Callable[[X], bool] = None, or_else: Callable[[], X | None] = None) -> X:
    """
    Finds the first value in a set/list that matches a predicate. Defaults to first index
    element if predicate doesn't match any value.

    :param iterable: the set/list in search.
    :param where: the predicate function to match the first value being searched.
    :param or_else: a fallback function if no value is found.
    :return: the first value found that matches the predicate or the first index element.
    """
    first_index_item = next(iter(iterable)) if or_else is None else or_else()
    return first_index_item if (where is None) else next(filter(where, iterable), first_index_item)


def last(iterable: set[X] | list[X], where: Callable[[X], bool] = None) -> X:
    """
    Finds the last value in a set/list that matches a predicate. Defaults to last index
    element if predicate doesn't match any value.

    :param iterable: the set/list in search.
    :param where: the predicate function to match the last value being searched.
    :return: the last value found that matches the predicate or the last index element.
    """
    reversed_iterable = reversed(iterable)
    last_index_item = next(iter(reversed_iterable))

    return last_index_item if (where is None) else next(filter(where, last_index_item), last_index_item)


def join_lines(iterable: Iterable[str]):
    """
    Combines a group of lines in a single string.

    :param iterable: the group of lines to combine.
    :return: a single string that is the result of the line's combination.
    """
    return join(iterable, "\n")


def join(iterable: Iterable[str], separator: str = " "):
    """
    Combines a group of strings in a single string.

    :param iterable: the group of strings to combine.
    :param separator: what to put between strings.
    :return: a single string that is the result of the line's combination.
    """
    return separator.join(iterable)


def get_or_else(x: X | None, or_else: Callable[[], X]) -> X:
    """
    Checks if a value is None, and if it is, calls :param:`or_else` callback.

    :param x: the value to check
    :param or_else: the callback that must return a non None value
    :return: a non None value
    """
    return x or or_else()


def safe_string(x: str | None) -> str:
    """
   Checks if a string is none, and if so, returns an empty string

   :param x: the possible None string
   :return: the received string or an empty string
   """
    return get_or_else(x, lambda: "")


def safe_set(x: set[X] | None) -> set[X]:
    """
    Checks if a set is none, and if so, returns an empty set

    :param x: the possible None set
    :return: the received set or an empty set
    """
    return get_or_else(x, lambda: set[X]())


def safe_list(x: list[X] | None) -> list[X]:
    """
    Checks if a list is none, and if so, returns an empty list

    :param x: the possible None list
    :return: the received list or an empty list
    """
    return get_or_else(x, lambda: list[X]())


def file_contains_value(file_path: str, value: str, mode="r") -> bool:
    """
    Validates whether a specific file constains a specific value using Python builtins.

    :param file_path: path that locates the file in the filesystem.
    :param value: the value to be searched in the file, as a string (plaintext)
    :param mode: the file read/write mode. defaults to "r" (read)
    """
    with(open(file_path, mode) as file):
        return file.read().find(value)