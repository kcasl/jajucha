#!/usr/bin/env python3

import cv2
import depthai as dai
import socket
import pickle

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")

# Properties
camRgb.setPreviewSize(640,480)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
camRgb.preview.link(xoutRgb.input)


#UDP server
UDP_IP = '192.168.12.1'
UDP_PORT = 9848

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((UDP_IP,UDP_PORT))

print("UDP server is listening...")

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    print('Connected cameras:', device.getConnectedCameraFeatures())
    # Print out usb speed
    print('Usb speed:', device.getUsbSpeed().name)
    # Bootloader version
    if device.getBootloaderVersion() is not None:
        print('Bootloader version:', device.getBootloaderVersion())
    # Device name
    print('Device name:', device.getDeviceName())

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    while True:
        data, client_address = udp_sock.recvfrom(1024)
        while True:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
            resized = inRgb.getCvFrame()
            resized = cv2.Canny(resized,100,200)

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),30]
            image_data = cv2.imencode('.jpg',resized,encode_param)[1].tobytes()
            udp_sock.sendto(image_data,(client_address))
            print(image_data)
            #print(client_address)


            # Retrieve 'bgr' (opencv format) frame
            cv2.imshow("rgb", resized)

            if cv2.waitKey(1) == ord('q'):
                break