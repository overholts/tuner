import logging
import os
import re
from abc import abstractmethod
from pathlib import Path
from typing import Dict, Set


TEMPLATE_PATTERN = re.compile("{([^/}]+)}")

logger = logging.getLogger("ParameterizedPathResolver")


class ParameterizedPathResolver:
    """
    Path resolver which uses a template to generate dynamic output paths at runtime.
    """

    @abstractmethod
    def __init__(self, path_template: Path):
        """
        Instantiate a new parameterized path resolver. Clients should
        validate that they are capable of generating all required parameters
        (as specified by the `path_parameters` member) at instantiation time,
        if possible.

        Missing parameters will result in a ValueError at runtime, and
        extraneous parameters will be ignored.

        Path template parameters are denoted by curly braces, and may comprise
        some or all of a path segment::

            /hello/{parameter1}/world/{parameter2}.ext
            /hello/{parameter1}_world/file.ext

        Path templates should be an absolute path. We assume docker-compose mounting
        can handle relative paths if needed.

        :param path_template: the path template string.
        """

        if not os.path.isabs(path_template):
            raise ValueError(
                f"Path template '{path_template}' does not represent an absolute path!"
            )

        self.path_template = str(path_template)  # need to leverage str methods
        self.path_parameters = self.__parse_path_parameters(self.path_template)

        logger.debug(
            f"Extracted parameters {self.path_parameters} from {path_template}"
        )

    def get_path(self, parameters: Dict[str, str]) -> Path:
        return Path(self.__render_path_template(parameters))

    def __render_path_template(self, parameters) -> str:
        missing_parameters = self.path_parameters.difference(set(parameters.keys()))
        logger.debug(
            f"Resolving path template '{self.path_template}' with parameters: {parameters}"
        )
        if missing_parameters != set():
            raise ValueError(
                f"Missing required parameters to construct output path: {missing_parameters}"
            )

        materialized_path = self.path_template
        for key in self.path_parameters:
            materialized_path = materialized_path.replace(f"{{{key}}}", parameters[key])

        return materialized_path

    @staticmethod
    def __parse_path_parameters(template_string) -> Set[str]:
        return set(TEMPLATE_PATTERN.findall(template_string))
