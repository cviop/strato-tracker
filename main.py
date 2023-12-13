from typing import Tuple
from SerialHandler import SerialHandler
from DemoSerialHandler import DemoSerialHandler
from matplotlib import pyplot as plt
import argparse
from gmplot import gmplot
import os
from selenium import webdriver
import time
import tkinter as Tk
import os


parser = argparse.ArgumentParser(description="Visualization of GPS data from Jakub Dvořák stratospheric probe.")
parser.add_argument("--port", help="Name of serial port of the receiver from GPS probe", default="COM9", type=str, required=False)
parser.add_argument("--debug", help="Enable debug mode of visualization", default=False, action="store_true", required=False)
args = parser.parse_args()
LEFT_BOTTOM_CORNER = (14.382810, 50.098527)   # (longitude, latitude) 50.098527, 14.382810
RIGHT_TOP_CORNER = (14.409875, 50.107141)     # (longitude, latitude) 
MAP_WIDTH = 1507
MAP_HEIGHT = 748


def main():
    debug = args.debug  # no debug in basic format
    serial_port = args.port  # default value of serial port
    gmap = gmplot.GoogleMapPlotter(50.1027458,14.3935679,16.62) #center map to Dejvice 50.10203861110547, 14.39183530621543, 18 or Home 50.09586110952633, 14.35383599064989
    #os.system('start .\my_map.html')
    gmap.draw("my_map.html")

    clear = lambda: os.system('cls')

    driver = webdriver.Firefox(executable_path=r'C:\Users\dvorakj\Documents\geckodriver.exe')
    driver.get('file:///C:/Users/dvorakj/Documents/GitHub/strato-tracker/my_map.html')

    wait_to_refresh = 0
    #mytext = Tk.StringVar()
    #mytext.set("First")

    #label = Tk.Label(None, textvariable=mytext, font=('Times', '18'),fg='blue')


    # Create serial connection handler
    if debug:
        handler = DemoSerialHandler(serial_port, 19200)
    else:
        handler = SerialHandler(serial_port, 19200)

    try:
        while True:
            # Get new data
            new_data = handler.getNewData()
            # Skip current iteration in the loop, if new data is invalid
            if new_data is None:
                continue
            
            # Update plot
            clear()
            print(f"\rGPS: {new_data[0]}N, {new_data[1]}E\nAlt: {new_data[2]} m\nSpeed: {new_data[3]} km/h\nTemp: {new_data[4]} C")
            gmap.marker(new_data[1], new_data[0], 'cornflowerblue')
            gmap.draw("my_map.html")
            if wait_to_refresh > 60:
                driver.refresh()
                wait_to_refresh = 0
            wait_to_refresh += 1
            #label.config(textvariable=new_data[0])
            #label.pack()
            #label.update_idletasks()
            #label.update()
            #plt.scatter(scatter_locations_x, scatter_locations_y, marker=".")
    except KeyboardInterrupt:
        handler.close()


# Map from GPS data to pixels on matplotlib plot, top left corner is (0, 0) in px coordinates
def coordinates_to_pixels(coordinates: Tuple[float, float]) -> Tuple[float, float]:
    width_long = RIGHT_TOP_CORNER[0] - LEFT_BOTTOM_CORNER[0]
    height_lat = RIGHT_TOP_CORNER[1] - LEFT_BOTTOM_CORNER[1]

    x_px = MAP_WIDTH * (coordinates[0] - LEFT_BOTTOM_CORNER[0]) / width_long
    y_px = MAP_HEIGHT - MAP_HEIGHT * (coordinates[1] - LEFT_BOTTOM_CORNER[1]) / height_lat

    return x_px, y_px


if __name__ == '__main__':
    main()
