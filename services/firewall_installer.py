import ctypes

from core.utils import resource_path


class FirewallInstaller:

    @staticmethod
    def install():

        script = resource_path(
            "assets/scripts/relay_firewall.cmd"
        )

        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            "cmd.exe",
            f'/c "{script}"',
            None,
            1
        )