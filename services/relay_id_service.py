

import re


class RelayIdService:

    @staticmethod
    def ip_to_id(ip: str) -> str:
        """
        Convert IPv4 address to Relay ID.
        Example:
            192.168.1.10
            ->
            1109 9261 8100
        """

        octets = ip.split(".")

        octets = [octet.zfill(3) for octet in octets]

        relay_id = ""

        for digit_index in range(3):
            for octet in octets:
                relay_id += octet[digit_index]

        return (
            relay_id[:4]
            + " "
            + relay_id[4:8]
            + " "
            + relay_id[8:]
        )

    @staticmethod
    def id_to_ip(relay_id: str) -> str:
        """
        Convert Relay ID back to IPv4.
        """

        relay_id = RelayIdService.normalize_relay_id(
            relay_id
        )

        relay_id = relay_id.replace(" ", "")

        octets = [""] * 4

        for digit_index in range(3):
            for i in range(4):
                octets[i] += relay_id[
                    i + digit_index * 4
                ]

        octets = [
            str(int(octet))
            for octet in octets
        ]

        return ".".join(octets)

    @staticmethod
    def normalize_relay_id(
        relay_id: str
    ) -> str:
        """
        Remove spaces and dashes.
        """

        relay_id = relay_id.strip()

        relay_id = relay_id.replace(
            " ",
            ""
        )

        relay_id = relay_id.replace(
            "-",
            ""
        )

        return relay_id

    @staticmethod
    def is_valid_ip(
        ip: str
    ) -> bool:

        try:

            octets = ip.split(".")

            if len(octets) != 4:
                return False

            for octet in octets:

                value = int(octet)

                if value < 0 or value > 255:
                    return False

            return True

        except ValueError:

            return False

    @staticmethod
    def is_valid_relay_id(
        relay_id: str
    ) -> bool:

        relay_id = RelayIdService.normalize_relay_id(
            relay_id
        )

        return bool(
            re.fullmatch(
                r"\d{12}",
                relay_id
            )
        )