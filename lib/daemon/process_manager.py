import logging
import signal

logger = logging.getLogger("ProcessManager")


class ProcessManager:
    def __init__(self):
        logger.debug(
            "Initialized process manager. Listening for system process signals."
        )
        signal.signal(signal.SIGINT, self.__set_terminate)
        signal.signal(signal.SIGTERM, self.__set_terminate)
        self.__terminate = False

    def __set_terminate(self, signum, _frame):
        logger.debug(f"Received signal {signum}. Attempting to shut down gracefully...")
        self.__terminate = True

    def should_terminate(self) -> bool:
        return self.__terminate
