from datetime import datetime

from lib.library.parameterized_path_resolver import ParameterizedPathResolver


class DatetimePathResolver:
    """
    Path resolver which supports paths parameterized with standard `strftime` format codes.
    """

    def __init__(self, path_resolver: ParameterizedPathResolver):
        self._path_resolver = path_resolver

    def get_path(self, time: datetime):
        date_parameters = {
            param: time.strftime(param) for param in self._path_resolver.path_parameters
        }
        return self._path_resolver.get_path(date_parameters)
