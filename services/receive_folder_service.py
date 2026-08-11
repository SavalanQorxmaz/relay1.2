"""
Relay 1.2

Receive Folder Service
"""

import os
import subprocess
from pathlib import Path

from core.settings import RECEIVE_FOLDER_NAME
from services.config_service import ConfigService


class ReceiveFolderService:

    CONFIG_KEY = "receive_folder"

    @classmethod
    def get_default_path(cls) -> Path:

        documents = (
            Path(os.environ["USERPROFILE"])
            / "Documents"
        )

        return documents / RECEIVE_FOLDER_NAME

    @classmethod
    def get_path(cls) -> Path:

        saved_path = ConfigService.get(cls.CONFIG_KEY)

        if saved_path:

            path = Path(saved_path).resolve()

        else:

            path = cls.get_default_path().resolve()

            ConfigService.set(
                cls.CONFIG_KEY,
                str(path)
            )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    @classmethod
    def set_path(cls, path: Path):

        path = Path(path).resolve()

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        ConfigService.set(
            cls.CONFIG_KEY,
            str(path)
        )

    @classmethod
    def open_folder(cls):

        subprocess.run(
            [
                "explorer",
                str(cls.get_path())
            ]
        )