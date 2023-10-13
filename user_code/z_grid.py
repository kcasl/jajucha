import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import library.control
import library.img_process as process
import depthai as dai
import cv2
import setproctitle

def set_unique_process_name(unique_name):
    setproctitle.setproctitle(unique_name)

def steering_reverse(steering,speed):
    speed = 100-speed
    steering = 90-steering
            
    if(steering < 25):
        steering = 28
    elif(steering > 65):
        steering = 62
    return steering,speed

def main_loop():
    with dai.Device(jajucha.pipeline) as device:
        qRgb = device.getOutputQueue(name = 'rgb', maxSize = 4,blocking = False)
        print("jajuchaready") #do not delete this line
        data , client_address = jajucha.udp_sock.recvfrom(1024)
        print("jajucharunning")
        while True:
            resized = jajucha.image_get(qRgb)
            
            (V,L,R),resized = process.gridFront(resized)
            
            
            # print('0',(L[0] + R[0]) /2)
            # print('1',(L[1] + R[1]) /2)
            # print('2',(L[2] + R[2]) /2)

            # # 321
            
            # if (L[0] + R[0]) /2 < 
            
    
            #speed = 50/ +- 50
            #steerin g = 45 +- 23
            #ssh -> 192.168.12.1
            
            if(V[3] < 120):
                speed = 53
                steering = 45
            else:
                speed = 53
                steering = 45
                
            if (L[1] - R[1]) < 1: 
                w = L[1] - R[1] * -0.02
                steering += w 
            elif (L[1] - R[1]) > 1:
                w = L[1] - R[1] * 0.02
                steering -= w 
                
           
            
            #Min steer = 25 #Max steer = 65 #middle  = 45 
            # middle_speed = 50 , max = 10 , reverse_max = 90
            
            #steering = 45
            #speed = 40
            
            
            
            
            
            
            
            
            
            #steering #speed reverse compensation
            steering,speed = steering_reverse(steering,speed)
            jajucha.control(steering,steering,speed)
            jajucha.image_send(resized,client_address)

                
                       
if __name__ == "__main__":
    unique_name = "user_program"
    set_unique_process_name(unique_name)
    
    jajucha = library.control.control()
    jajucha.control(45,45,50)
    
    main_loop()
    