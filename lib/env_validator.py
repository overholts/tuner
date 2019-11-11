import logging
import os
import textwrap

logger = logging.getLogger("EnvironmentValidator")


def validate_env():
    if not ("TZ" in os.environ and os.environ["TZ"].strip()):
        logger.error(
            (
                "'TZ' environment variable is not set! "
                "Please use the '--env , -e' argument with docker run to pass the host's local time zone. "
                "This is required explicitly because a mismatch between host time and container timezone "
                "will completely break the desired behavior of the application. See README for more information."
            )
        )
        return False

    logger.debug("All validations passed!")
    return True
