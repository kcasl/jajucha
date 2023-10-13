#!/usr/bin/env python3
import setproctitle
import cv2
import depthai as dai
import socket
import pickle
import struct
import serial
import time
import signal
import threading


port = '/dev/ttyTHS2' #serial port
baud = 576000 #serial baudrate
UDP_IP = '192.168.12.1'
UDP_PORT = 9848



class control:
    def __init__(self):
        
        self.ser = serial.Serial(port, baud, timeout=0)
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind((UDP_IP,UDP_PORT))

        self.pipeline = dai.Pipeline()

        # Define source and output
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)

        self.xoutRgb.setStreamName("rgb")

        # Properties
        self.camRgb.setPreviewSize(640,480)
        self.camRgb.setInterleaved(False)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        self.camRgb.setFps(30)

        # Linking
        self.camRgb.preview.link(self.xoutRgb.input)
        
    
    def control(self,left_arm,right_arm,velocity,mode = 9):
        
        lat = (int)(left_arm/10)
        lao = left_arm-lat*10

        rat = (int)(right_arm/10)
        rao = right_arm-rat*10

        vt = (int)(velocity/10)
        vo = velocity-vt*10

        mt = (int)(mode/10)
        mo = mode-mt*10


        li = [str(lat),str(lao),str(rat),str(rao),str(vt),str(vo),str(mt),str(mo)]
        li = ''.join(li)

        self.ser.write(str.encode(li))
        time.sleep(0.01)

    def image_get(self,qRgb):
        inRgb = qRgb.get()
        try:
            output = inRgb.getCvFrame()
        except:
            pass
        return output

    def image_send(self,resized,client_address):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),30]
        image_data = cv2.imencode('.jpg',resized,encode_param)[1].tobytes()
        self.udp_sock.sendto(image_data,(client_address))

    def joy_get_thread(self):
        while(True):
            data, client_address = self.udp_sock.recvfrom(8)
            print("joy_received")
            vel = 0
            steer = 0

            try:
                float_value1 = struct.unpack('!ff',data)[0]
                float_value2 = struct.unpack('!ff',data)[1]
                vel = (float_value2*50)+50
                steer = 45-float_value1*20

                #print(int(vel),steer)

                if(vel < 10):
                    vel = 10
                elif(vel > 90):
                    vel = 90
                self.control(int(steer),int(steer),int(vel),9)
                time.sleep(0.01)
                        # if(vel == 50):
                        #     jajucha_control(int(steer),int(steer),int(vel),0)
                        # else:           
            except:
                pass




