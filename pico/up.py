###Test kodu
from dalay import dalay
import select
import sys
import machine
import utime
import time         #time library for sleep
dalay = dalay(50,0,11,12,19,4,20)#pinleri belirt 50 freq digerleri 0,1,2,3,4,5 pin
from machine import Pin
led = Pin(25, Pin.OUT)
led.on()
wss=0
ch = ""
while True:
    wss+=1
    if wss == 1:
       print("calibration")
       dalay.calibration()
    else:
        dalay.stopup()
        dalay.stop()
        dalay.wait()
        time.sleep(2)
        dalay.control(1,1,0)
        


