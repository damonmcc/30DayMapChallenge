import logging


def setup_logging(logging_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger()
    logging_level = logging._nameToLevel[logging_level]
    logging.basicConfig(level=logging_level)

    return logger


def log_header(logger, text: str):
    logger.info("=" * 5 + f" {text} " + "=" * 5)
