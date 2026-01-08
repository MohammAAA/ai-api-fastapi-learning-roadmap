import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    root = logging.getLogger() # Create a logger instance called root
    root.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        "logs/assistant_requests.log",
        maxBytes=5_000_000,
        backupCount=5, # determines the number of old log files to keep when a log rotation occurs.
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s") # The log format will be ("log time" "log level: info, warn, error" "module name that writes the log (e.g.: personal_assistant_api)" "Log message")
    handler.setFormatter(formatter)

    # avoid duplicate handlers on reload
    if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        root.addHandler(handler)