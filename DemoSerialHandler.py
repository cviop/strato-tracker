import time

from ABCSerialReader import ABCSerialReader
from random import random, seed


class DemoSerialHandler(ABCSerialReader):
    last_longitude = 50.0796694
    last_latitude = 14.4370942

    def __init__(self, port: str, baud_rate: int):
        super().__init__(port, baud_rate)
        # set some seed to have repeatable results
        seed(baud_rate)

    def getNewData(self):
        time.sleep(1)

        self.last_longitude += (2 * random() - 1) / 40
        self.last_latitude += (2 * random() - 0.5) / 40

        return self.last_latitude, self.last_longitude

