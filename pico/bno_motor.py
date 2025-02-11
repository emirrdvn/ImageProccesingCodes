
import machine
import time
from bno055_base import BNO055_BASE
import select
import sys
import utime
from dalay import dalay

dalay = dalay(50,0,11,12,19,4,20)#pinleri belirt 50 freq digerleri 0,1,2,3,4,5 pin
from machine import Pin
led = Pin(25, Pin.OUT)
led.on()
wss=0
ch = ""
i2c = machine.I2C(0,sda=machine.Pin(8), scl=machine.Pin(9),freq=4000)
imu = BNO055_BASE(i2c)
calibrated = False
c=0
file=open("bnovalue.txt","w")	# creation and opening of a CSV file in Write mode
while True:
    
    wss+=1
    if wss == 1:
       print("calibration")
       dalay.calibration()
    else:
        
        if not calibrated:
            calibrated = imu.calibrated()
            #print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
        #print('sıcaklık {}°C'.format(imu.temperature()))
        #print('Mıknatıslanma       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
        print('jiroskop                x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
        #print('ivme                x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
        #print('hızlanma vektoru    x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
        #print('yer çekimi ivmesi   x {:5.1f}    y {:5.1f}     z {:5.6f}'.format(*imu.gravity()))#+
        print('Heading  {:4.1f} roll {:4.1f} pitch {:4.1f}'.format(*imu.euler()))
        time.sleep(0.1)
        jiroskop='J {:5.0f} {:5.0f} {:5.0f}'.format(*imu.gyro())
        head='H {:4.1f} r {:4.1f} p {:4.1f}'.format(*imu.euler())
        gravity='Y {:5.1f} {:5.1f} {:5.6f}'.format(*imu.gravity())
        file.write(str(jiroskop)+"\n"+str(head)+"\n"+str(gravity)+"\n")	# Writing data in the opened file
        file.flush()
        c+=1
        if(43<int(head[2:4])<48):
            dalay.forward()
            print(head[2:4])
        else:
            dalay.turnleft()
