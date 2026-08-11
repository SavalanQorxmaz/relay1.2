from enum import Enum, auto


class AppState(Enum):

    READY = auto()

    OUTGOING_REQUEST = auto()

    INCOMING_REQUEST = auto()

    CONNECTED = auto()

    TRANSFERRING = auto()

    COMPLETED = auto()

    ERROR = auto()