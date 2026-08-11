"""
Relay 1.2

Resource Path
"""

from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    return Path(relative_path)