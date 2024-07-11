import logging

TASK_LEVEL = 25
logging.addLevelName(TASK_LEVEL, "TASK")

def task(self, message, *args, **kws):
    if self.isEnabledFor(TASK_LEVEL):
        self._log(TASK_LEVEL, message, args, **kws)
logging.Logger.task = task

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    purple = "\x1b[35;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = "[%(asctime)-23s] [%(levelname)s] %(message)-50s (%(filename)s:%(lineno)-d)\n"

    FORMATS = {
        logging.DEBUG: purple + _format + reset,
        logging.INFO: green + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
        TASK_LEVEL: purple + _format + reset  
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.grey + self._format + self.reset)
        formatter = logging.Formatter(log_fmt, style='%')
        return formatter.format(record)

logger = logging.getLogger("Link-ML-Service")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
logger.propagate = False
logger.addHandler(ch)

