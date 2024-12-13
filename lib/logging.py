LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
        "console": {
            "format": "%(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "file",
            "filename": "script.log",
            "mode": "a",  # Append to the log file
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "console",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "DEBUG",  # Root logger captures all logs
        "handlers": ["file_handler", "console_handler"],
    },
}
