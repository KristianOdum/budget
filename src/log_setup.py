import logging
import sys

class CustomFormatter(logging.Formatter):
    LEVEL_MAP = {
        'VERBOSE': 'V',
        'DEBUG': 'D',
        'INFO': 'I',
        'WARNING': 'W',
        'ERROR': 'E',
        'CRITICAL': 'C'
    }

    def format(self, record):
        # Map levelname to single char
        record.levelname = self.LEVEL_MAP.get(record.levelname, record.levelname[0])
        # Truncate or pad filename and funcName
        record.filename = f"{record.filename[:16]:>16}"
        record.funcName = f"{(record.funcName[:12]):<12}"
        return super().format(record)

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("log.txt")
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)

# formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(name)s] %(message)s', datefmt='%H:%M:%S')
formatter = CustomFormatter('[%(levelname)s] [%(filename)s:%(funcName)s] %(message)s', datefmt='%H:%M:%S')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

getLogger = logging.getLogger
