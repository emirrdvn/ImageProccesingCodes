#araç yamulduğunda tespit eden ve düzleyen algoritma ##First PID
from turtle import forward
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
dalay = dalay(50,0,11,12,19,4,20)#pinleri belirt 50 freq digerleri 0,1,2,3,4,5 pin
led = Pin(25, Pin.OUT)
led.on()
wss=0
ch = ""
i2c = machine.I2C(0,sda=machine.Pin(8), scl=machine.Pin(9),freq=4000)
imu = BNO055_BASE(i2c)
calibrated = False
c=""
komut=""
e_angle=0
while True:
    wss+=1
    if wss == 1:
       print("calibration")
       dalay.calibration()
    else:
        if not calibrated:
            calibrated = imu.calibrated()
            f_imu = imu.euler()[0]
            if f_imu != 0:
                calibrated = True
        else:
            time.sleep(0.1)
            ###########################
            #hizlanma ivmesi alınacak
            heuler=conversion(imu.euler()[0],f_imu)
            di = 0
            if heuler>180:
                di = 1
                e_angle = 360-int(heuler)
                e_pwm = e_angle*2.5
                dalay.forward_control(e_pwm,di)
            else:
                di=0
                e_angle=int(heuler)
                e_pwm=e_angle*2.5
                dalay.forward_control(e_pwm,di)