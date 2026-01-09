import os
import csv
import logging
from datetime import datetime

class CSVPromptHandler(logging.Handler):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

        # Create file + header once (if empty/new)
        file_exists = os.path.exists(filename)
        if (not file_exists) or os.path.getsize(filename) == 0:
            with open(filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "module", "prompt", "response", "model", "totalTokens"])

    def emit(self, record: logging.LogRecord) -> None:
        # Expect prompt/response attached via `extra={...}`
        prompt = getattr(record, "prompt", "")
        response = getattr(record, "response", "")
        model = getattr(record, "model", "")
        total_tokens = getattr(record, "totalTokens", "")

        ts = datetime.utcfromtimestamp(record.created).isoformat() + "Z"
        module_name = record.name

        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([ts, module_name, prompt, response, model, total_tokens])


def setup_csv_logging(csv_path: str = "logs/assistant_prompts.csv", level: int = logging.INFO) -> None:
    logger = logging.getLogger("appLoger.csv")
    logger.setLevel(level)
    logger.propagate = False  # don't send to root
    logging.getLogger("httpx").setLevel(logging.WARNING) # This promotes the httpx log messages to be of WARNING severity so that these logs are not shown in our log file


    handler = CSVPromptHandler(csv_path)
    handler.setLevel(level)

    # Avoid duplicate handlers (common with reload)
    if not any(isinstance(h, CSVPromptHandler) and getattr(h, "filename", None) == csv_path for h in logger.handlers):
        logger.addHandler(handler)