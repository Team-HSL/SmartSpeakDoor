import serial
from serial.tools import list_ports
import sys
import io
from PIL import Image
from PIL import ImageDraw
from matplotlib import pyplot as plt
import numpy as np
import cv2

ports = list_ports.comports()

ser = serial.Serial()
ser.baudrate = 9600
print(ports)
ser.port = ports[0].device
ser.open()


jpg = []
# cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)
while True:
    barray  = ser.read(13)
    barray = np.fromstring(barray,dtype="uint8")
    print(barray)
    # b_list = barray.split(b'\xff\xd8')
    # cut_bynary = b_list[1].partition(b'\xff\xd9')
    # cut_bynary_modified = bytes().join([b'\xff\xd8',cut_bynary[0],b'\xff\xd9'])

    # cv2.imshow("Capture",cv2.imdecode(np.fromstring(cut_bynary_modified,dtype="uint8"), -1))

    # cv2.waitKey(33)
ser.close()
