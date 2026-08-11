"""
Relay 1.2

Configuration Service
"""

import json
from pathlib import Path


class ConfigService:

    CONFIG_FILE = (
        Path(__file__).parent.parent
        / "config"
        / "config.json"
    )

    @classmethod
    def load(cls) -> dict:

        if not cls.CONFIG_FILE.exists():
            return {}

        with open(
            cls.CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @classmethod
    def save(cls, data: dict):

        cls.CONFIG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            cls.CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    @classmethod
    def get(cls, key, default=None):

        return cls.load().get(
            key,
            default
        )

    @classmethod
    def set(cls, key, value):

        data = cls.load()

        data[key] = value

        cls.save(data)