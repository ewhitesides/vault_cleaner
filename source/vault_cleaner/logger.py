"""
logger
"""

import logging

#creates parent logger with base config for child loggers to inherit
PARENT_LOG_NAME='vault_cleaner'

logger = logging.getLogger(PARENT_LOG_NAME)
logger.setLevel(logging.DEBUG)

#using this format so splunk picks up the fields automatically
formatter = logging.Formatter(
    fmt='Time="%(asctime)s", Module="%(name)s", Level="%(levelname)s", Message="%(message)s"',
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)

#define console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

#add handlers to instance 'logger'
logger.addHandler(console_handler)
