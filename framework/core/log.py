import logging
from abc import ABC, abstractmethod


class LumberSnakeClient(ABC):
    """
    Defines the behavior of a logging client
    """

    @abstractmethod
    def log_info(self, message: str) -> None:
        """
        Logs an informational message.

        :param message: the message to be logged.
        """

    @abstractmethod
    def log_warning(self, message: str) -> None:
        """
        Logs a warning message.

        :param message: the message to be logged.
        """

    @abstractmethod
    def log_error(self, message: str, error: BaseException) -> None:
        """
        Logs an error message.

        :param message: the message to be logged.
        :param error: the error to be logged.
        """

    @abstractmethod
    def log_fatal(self, message: str) -> None:
        """
        Logs a fatal message.

        :param message: the message to be logged.
        """


class ConsoleLumberSnakeClient(LumberSnakeClient):
    """
    A :class:`LumberSnakeClient` that logs to the console/stdin.
    """

    def log_info(self, message: str) -> None:
        print(f"[info]: {message}")

    def log_warning(self, message: str) -> None:
        print(f"[warning]: {message}")

    def log_error(self, message: str, error: BaseException) -> None:
        print(f"[error]: {message} | {error}")

    def log_fatal(self, message: str) -> None:
        print(f"[fatal]: {message}")


# Global list of logging clients
__clients__: list[LumberSnakeClient] = []


def put_snakes_to_work(clients: list[LumberSnakeClient]):
    """
    Registers logging clients to receive logging calls.

    :param clients: the list of :class:`LumberSnakeClient` to register
    """

    __clients__.clear()
    __clients__.extend(clients)


def log_info(message: str):
    """
    Logs an informational message.

    :param message: the message to be logged.
    """

    for client in __clients__:
        client.log_info(message)


def log_warning(message: str):
    """
    Logs a warning message.

    :param message: the message to be logged.
    """

    for client in __clients__:
        client.log_warning(message)


def log_error(message: str, error: BaseException):
    """
    Logs an error message.

    :param message: the message to be logged.
    :param error: the error to be logged.
    """

    for client in __clients__:
        client.log_error(message, error)


def log_fatal(message: str):
    """
    Logs a fatal message.

    :param message: the message to be logged.
    """

    for client in __clients__:
        client.log_fatal(message)
