

from enum import Enum   

class TransferState(Enum):

    IDLE

    PREPARING

    WAITING

    SENDING

    RECEIVING

    CANCELLED

    COMPLETED

    FAILED