import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import library.control
import library.img_process as process
import depthai as dai
import cv2
import setproctitle
import motorlib as ml
import time
import math

def set_unique_process_name(unique_name):
    setproctitle.setproctitle(unique_name)

def main_loop():
    with dai.Device(jajucha.pipeline) as device:
        qRgb = device.getOutputQueue(name = 'rgb', maxSize = 4,blocking = False)
        print("jajuchaready") #do not delete this line
        data , client_address = jajucha.udp_sock.recvfrom(1024)
        print("jajucharunning")
        Last_mode = 'end_line'
        mode = "straight"
        Last_curve = "default"
        while True:

            resized = jajucha.image_get(qRgb)
        
            (V,L,R),resized = process.gridFront(resized)
            
            L_V_set = [V[0],V[1],V[2]]
            R_V_set = [V[4],V[5],V[6]]

            T_center = 320 - (L[2] - R[2])
            steering_const = 0.06
            steering = (320 - T_center) * steering_const
            steering = int(round(steering))
            
            if V[3] == 171 and abs(((L[1] + R[1])/2 + (L[0] + R[0])/2) - 440) <20 :
                mode = "straight"
                Last_mode = "straight"
            elif 171 not in V and V[6] < 156 and sum(L_V_set) < sum(R_V_set):
                mode = "R_curve"
                Last_mode = "right"
            elif 171 not in V and V[1] < 156 and sum(L_V_set) > sum(R_V_set):
                mode = "L_curve"
                Last_mode = "left"
            
            print(mode)
            
            if mode == 'default':
                mode = Last_mode
            if mode == 'straight':
                if V[3] <= 167:
                    ml.control(-steering,-steering,8,9)
                else:
                    ml.control(-steering,-steering,12,9)
            elif mode == 'R_curve':
                ml.control(15,15,8,9)
            elif mode == 'L_curve':
                ml.control(-15,-15,8,9)
         
            mode = "default"
            
            if V[3] == 0:
                break

            jajucha.image_send(resized,client_address)
            

if __name__ == "__main__":
    unique_name = "user_program"
    set_unique_process_name(unique_name)
    
    jajucha = library.control.control()
    jajucha.control(45,45,50)
    
    main_loop()
    