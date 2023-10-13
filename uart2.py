#Triangle Robotics 2023,Jajucha Core

import serial
import time
import signal
import threading


line = [] 

port = '/dev/ttyTHS1' #serial port
baud = 576000 #serial baudrate

exitThread = False 

def writeThread(ser):
    jajucha_control(45,45,55,10)
    
def jajucha_control(left_arm,right_arm,velocity,mode):

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

    ser.write(str.encode(li))
    time.sleep(0.05)

def handler(signum, frame):
     exitThread = True

def parsing_data(data):
    tmp = ''.join(data)
    print(tmp)

def readThread(ser):
    global line
    global exitThread

    while not exitThread:
        for c in ser.read():
            line.append(chr(c))
            #print(line)
            if c == 10: 
                parsing_data(line)
                
                del line[:]                

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)

    ser = serial.Serial(port, baud, timeout=0)

    thread = threading.Thread(target=readThread, args=(ser,))
    thread2 = threading.Thread(target=writeThread,args=(ser,))

    #start threads
    thread.start() #read thread
    thread2.start() #write thread
