import argparse
import logging
import sys
import textwrap
import time
from pathlib import Path

from lib.config import load_from_yaml
from lib.daemon.process_manager import ProcessManager
from lib.environment import Environment
from lib.scheduler.job_manager import JobManager
from lib.scheduler.recording_job import RecordingJob

logger = logging.getLogger("main")


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """\
        Tool for recording scheduled audio streams into a media library."""
        )
    )

    parser.add_argument(
        "-c",
        "--config",
        metavar="config",
        type=Path,
        required=True,
        help=textwrap.dedent(
            """\
            Configuration file location (yaml)"""
        ),
    )

    parser.add_argument(
        "-d",
        "--download-dir",
        metavar="download-dir",
        type=Path,
        required=False,
        default=Path("/downloads"),
        help=textwrap.dedent(
            """\
            Location to download raw audio files to."""
        ),
    )

    parser.add_argument(
        "-pd",
        "--pipeline-dir",
        metavar="pipeline-dir",
        type=Path,
        required=False,
        default=Path("/pipelined"),
        help=textwrap.dedent(
            """\
            Location to stage post-processed media files in. Staging them
            ensures that modifications of output media library directories
            are as transactional as possible. Data is only stored here
            transiently, so there is probably not normally a need to mount
            this directory outside of the container."""
        ),
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        help=textwrap.dedent(
            """\
            Enable verbose debugging output."""
        ),
    )

    return parser.parse_args(argv)


def initialize_logging(args):
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler(sys.stdout)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "[%(asctime)s] [PID %(process)d] [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(formatter)

    if args.verbose:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)

    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)


def main(argv=None):
    args = parse_args(argv)
    initialize_logging(args)
    process_manager = ProcessManager()

    logger.info("Running with args:")
    for arg in vars(args):
        logger.info(f"   {arg}:\t{getattr(args, arg)}")

    env = Environment()

    logger.debug(f"Loading config from {args.config}")
    config = load_from_yaml(args.config)

    job_manager = JobManager(env.timezone)

    # Create jobs for each source
    for source in config.sources:
        job_manager.register(RecordingJob(source, args.download_dir, args.pipeline_dir))

    # Begin execution of jobs
    job_manager.run()

    while not process_manager.should_terminate():
        time.sleep(1)

    job_manager.shutdown()

    logger.info("Shutting down.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
