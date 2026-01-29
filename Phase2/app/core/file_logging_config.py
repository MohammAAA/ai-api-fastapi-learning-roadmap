import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("appLoger.file") # Create a logger instance called appLogger.file
    logger.setLevel(logging.INFO)
    logger.propagate = False  # don't send to root (propagate = False stops the record from bubbling up to ancestor loggers (like root), which is a common way to prevent duplication and keep outputs separate.)
    handler = RotatingFileHandler(
        "logs/assistant_requests.log",
        maxBytes=5_000_000,
        backupCount=5, # determines the number of old log files to keep when a log rotation occurs.
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s %(extra_data)s") # The log format will be ("log time" "log level: info, warn, error" "module name that writes the log (e.g.: personal_assistant_api)" "logger.info's msg "the extra data in the 'extra' parameter in loggier.info")
    handler.setFormatter(formatter)

    # avoid duplicate handlers on reload
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        logger.addHandler(handler)