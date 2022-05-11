from abc import ABC
from typing import Any, Tuple


class ABCSerialReader(ABC):
    # Define some class variables
    # Incoming port of serial connection
    port: str
    # Baudrate of serial connection
    baud_rate: int
    # Internal opened handler of serial port
    handler: Any

    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate

    def getNewData(self) -> Tuple[float, float]:
        pass
