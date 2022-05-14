from typing import TextIO
from ABCSerialReader import ABCSerialReader
import serial
import time


class SerialHandler(ABCSerialReader):
    handler: serial.Serial
    file_handler: TextIO

    def __init__(self, port: str, baud_rate: int):
        super().__init__(port, baud_rate)
        self.handler = serial.Serial(port, baudrate=baud_rate)

        self.file_handler = open(f"serial_out_{int(time.time())}.csv", "w")

    def getNewData(self):
        try:
            new_data = self.handler.readline().decode(encoding="UTF-8")
        except UnicodeDecodeError:
            print("Couldn't parse new data")
            return None

        if new_data == "\n":
            return None

        parsed = []*24
        parsed = new_data.split(sep=";")

        # Assumption that we are always on the north-east side of globe
        try:
            longitude_str = parsed[3]
            latitude_str = parsed[1]
            alt = float(parsed[5])
            speed = float(parsed[6])
            temp1 = float(parsed[7])
        except:
            print("Couldn't parse new data")
            return None

        if longitude_str == "" or latitude_str == "":
            print("No GPS data")
            return None

        try:
            longitude = int(longitude_str[:3]) + float(longitude_str[3:]) / 60
            latitude = int(latitude_str[:2]) + float(latitude_str[2:]) / 60
        except ValueError:
            print("Invalid data")
            return None

        # Write new data only after everything is parsed
        self.file_handler.writelines(new_data)

        # Return new longitude and latitude
        return longitude, latitude, alt, speed, temp1

    def close(self):
        self.file_handler.close()


