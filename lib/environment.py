import logging
import os

from pytz import timezone

logger = logging.getLogger("EnvironmentValidator")


class Environment:
    def __init__(self):
        valid_env = True
        if not ("TZ" in os.environ and os.environ["TZ"].strip()):
            logger.error(
                (
                    "'TZ' environment variable is not set! "
                    "Please use the '--env , -e' argument with docker run to pass the host's local time zone. "
                    "This is required explicitly because a mismatch between host time and container timezone "
                    "will break the desired behavior of the application. See README for more information."
                )
            )
            valid_env = False
        else:
            self.timezone = timezone(os.environ["TZ"])

        if not valid_env:
            raise ValueError(
                "Environment requirements not met! See error logs for details."
            )

        logger.debug("All validations passed!")
