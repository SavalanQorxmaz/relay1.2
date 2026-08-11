"""
Relay 1.2

Firewall Service
"""

import subprocess

from core.settings import (
    FIREWALL_RULE_IN,
    FIREWALL_RULE_OUT,
)


class FirewallService:

    @classmethod
    def rule_exists(cls, rule_name: str) -> bool:

        result = subprocess.run(
            [
                "netsh",
                "advfirewall",
                "firewall",
                "show",
                "rule",
                f"name={rule_name}"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        return "Rule Name:" in result.stdout

    @classmethod
    def is_configured(cls) -> bool:

        return (
            cls.rule_exists(FIREWALL_RULE_IN)
            and
            cls.rule_exists(FIREWALL_RULE_OUT)
        )

    @classmethod
    def get_status(cls) -> str:

        if cls.is_configured():
            return "Configured"

        return "Not Configured"

    @classmethod
    def generate_batch(cls) -> str:

        return f"""@echo off

    netsh advfirewall firewall show rule name="{FIREWALL_RULE_IN}" >nul 2>&1

    if errorlevel 1 (
        netsh advfirewall firewall add rule ^
        name="{FIREWALL_RULE_IN}" ^
        dir=in ^
        action=allow ^
        protocol=TCP ^
        localport=5050
    )

    netsh advfirewall firewall show rule name="{FIREWALL_RULE_OUT}" >nul 2>&1

    if errorlevel 1 (
        netsh advfirewall firewall add rule ^
        name="{FIREWALL_RULE_OUT}" ^
        dir=out ^
        action=allow ^
        protocol=TCP ^
        localport=5050
    )

    exit
    """