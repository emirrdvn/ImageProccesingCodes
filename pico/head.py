###görüntü işleme ile hedef bulunana kadar aracın düz gitmesini sağlayan algoritma
import machine
import time
from bno055_base import BNO055_BASE
import select
import sys
import utime
from dalay import dalay
from machine import Pin


def conversion(x,f_head):
    if x>=f_head:
        return x-f_head
    else:
        return x+360-f_head

# def distance(trig,echo,sira):
#           trig = Pin(trig, Pin.OUT)
#           echo = Pin(echo, Pin.IN, Pin.PULL_DOWN)
#           trig.value(0)
#           time.sleep(0.1)
#           trig.value(1)
#           time.sleep_us(2)
#           trig.value(0)
#           while echo.value()==0:
#                pulse_start = time.ticks_us()
#           while echo.value()==1:
#                pulse_end = time.ticks_us()
#           pulse_duration = pulse_end - pulse_start
#           distance = pulse_duration * 17165 / 1000000
#           distance = round(distance, 0)
#           return distance
dalay = dalay(50,0,11,12,19,4,20)#pinleri belirt 50 freq digerleri 0,1,2,3,4,5 pin
led = Pin(25, Pin.OUT)
led.on()
wss=0
ch = ""
i2c = machine.I2C(0,sda=machine.Pin(8), scl=machine.Pin(9),freq=4000)
imu = BNO055_BASE(i2c)
calibrated = False
#f_imu_head = imu.euler()[0]
#print(f_imu)
#file=open("bnovalue.txt","w")	# creation and opening of a CSV file in Write mode
c=""
komut=""
while True:
    
    wss+=1
    if wss == 1:
       print("calibration")
       dalay.calibration()
       #f_imu = imu.euler()[0]
    else:
        
        if not calibrated:
            calibrated = imu.calibrated()
            f_imu = imu.euler()[0]
            if f_imu != 0:
                calibrated = True
        else:
            #print('sıcaklık {}°C'.format(imu.temperature()))
            #print('Mıknatıslanma       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
            #print('jiroskop                x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
            #print('ivme                x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
            #print('hızlanma vektoru    x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
            #print('yer çekimi ivmesi   x {:5.1f}    y {:5.1f}     z {:5.6f}'.format(*imu.gravity()))#+
            #print('Heading  {:4.1f} roll {:4.1f} pitch {:4.1f}'.format(*imu.euler()))
            time.sleep(0.1)
            jiroskop='J {:5.0f} {:5.0f} {:5.0f}'.format(*imu.gyro())
            head='H {:4.1f} r {:4.1f} p {:4.1f}'.format(*imu.euler())
            gravity='Y {:5.1f} {:5.1f} {:5.6f}'.format(*imu.gravity())
            #file.write(str(jiroskop)+"\n"+str(head)+"\n"+str(gravity)+"\n")	# Writing data in the opened file
            #file.flush()
            
            heuler=conversion(imu.euler()[0],f_imu)
            #distance3=distance1(18,17,3)
            print(heuler)
            if(40>heuler>2):
                komut="sol"
            elif(358>heuler>340):
                komut="sag"
            else:
                komut="ileri"
            print(komut)
            print(c)
        if(komut=="sag"):
            if(c!=komut):
                dalay.stop()
                dalay.wait()
                dalay.turnright(2)
        elif(komut=="sol"):
            if(c!=komut):
                dalay.stop()
                dalay.wait()
                dalay.turnleft(2)
        elif(komut=="ileri"):
            if(c!=komut):
                dalay.stop()
                dalay.wait()
                dalay.forward(2)
        c=komut
