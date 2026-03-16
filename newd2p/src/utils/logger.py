"""
newd2p - Logging Configuration
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_level: str = "INFO"):
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
               "<level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    Path("./logs").mkdir(exist_ok=True)

    logger.add(
        "./logs/newd2p.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )

    logger.add(
        "./logs/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="5 MB",
        retention="30 days",
    )

    logger.info("Logger initialized")
    return logger


def get_logger(module_name: str = "newd2p"):
    return logger.bind(module=module_name)
