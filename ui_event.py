from enum import Enum, auto


class UIEvent(Enum):

    CONNECT_CLICKED = auto()

    DISCONNECT_CLICKED = auto()

    SEND_CLICKED = auto()

    ACCEPT_CLICKED = auto()

    REJECT_CLICKED = auto()

    CANCEL_CLICKED = auto()

    BROWSE_CLICKED = auto()

    ABOUT_CLICKED = auto()