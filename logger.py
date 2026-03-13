"""
Cel-Logic Pro — Logging System
Internal logging for debugging production issues.
NOT for user-facing messages (use operator.report() for those).
"""

import logging

_logger = logging.getLogger("CelLogic")
_logger.setLevel(logging.DEBUG)

# Console handler
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter(
        "[CelLogic %(levelname)s] %(message)s"
    ))
    _logger.addHandler(_handler)


def info(msg):
    _logger.info(msg)


def warning(msg):
    _logger.warning(msg)


def error(msg):
    _logger.error(msg)


def debug(msg):
    _logger.debug(msg)
