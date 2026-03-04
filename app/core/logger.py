import sys
import json
from loguru import logger

def json_sink(message):
    record = message.record

    level = record["level"].name

    COLORS = {
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
        "RESET": "\033[0m"
    }
    log_record = {
        "timestamp": record["time"].isoformat(),
        "message": record["message"],
        **record["extra"]
    }

    serialized = json.dumps(log_record, ensure_ascii=False)
    color = COLORS.get(level, COLORS["RESET"])

    sys.stdout.write(f"{color}{serialized}{COLORS['RESET']}\n")

def setup_logging():
    logger.remove()
    logger.add(json_sink)

setup_logging()