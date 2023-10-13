import serial
import time

port = '/dev/ttyTHS2' #serial port
baud = 576000 #serial baudrate

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
    #time.sleep(0.1)

ser = serial.Serial(port, baud, timeout=0)
for x in range(3):
    jajucha_control(45,45,50,9)
    time.sleep(0.01)
jajucha_control(45,45,50,0)
print("executed")


exit()