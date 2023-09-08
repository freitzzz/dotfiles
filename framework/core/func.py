from typing import TypeVar, Callable

X = TypeVar('X')


def first(iterable: set[X] | list[X], where: Callable[[X], bool]) -> X:
    """
    Finds the first value in a set/list that matches a predicate.

    :param iterable: the set/list in search.
    :param where: the predicate function to match the first value being searched.
    :return: the first value found that matches the predicate.
    """
    return next(filter(where, iterable))


def get_or_else(x: X | None, or_else: Callable[[], X]) -> X:
    """
    Checks if a value is None, and if it is, calls :param:`or_else` callback.

    :param x: the value to check
    :param or_else: the callback that must return a non None value
    :return: a non None value
    """
    return x or or_else()


def safe_set(x: set[X] | None) -> set[X]:
    """
    Checks if a set is none, and if so, returns an empty set

    :param x: the possible None set
    :return: the received set or an empty set
    """
    return get_or_else(x, lambda: set[X]())
