import logging
import sys
from google.cloud.logging_v2.handlers import ContainerEngineHandler


_logger = None


# Implemented like TensorFlow logger:
# https://github.com/tensorflow/tensorflow/blob/v2.4.1/tensorflow/python/platform/tf_logging.py#L93-L143
def get_logger() -> logging.Logger:

    global _logger

    if not _logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(ContainerEngineHandler(stream=sys.stderr))
        _logger = logger

    return _logger
