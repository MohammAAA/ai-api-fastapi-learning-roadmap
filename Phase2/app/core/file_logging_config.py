import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    root = logging.getLogger() # Create a logger instance called root
    root.setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING) # This promotes the httpx log messages to be of WARNING severity so that these logs are not shown in our log file


    handler = RotatingFileHandler(
        "logs/assistant_requests.log",
        maxBytes=5_000_000,
        backupCount=5, # determines the number of old log files to keep when a log rotation occurs.
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s %(extra_data)s") # The log format will be ("log time" "log level: info, warn, error" "module name that writes the log (e.g.: personal_assistant_api)" "logger.info's msg "the extra data in the 'extra' parameter in loggier.info")
    handler.setFormatter(formatter)

    # avoid duplicate handlers on reload
    if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        root.addHandler(handler)