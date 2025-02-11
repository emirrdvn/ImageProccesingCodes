###Havuzda denenmek üzere yazılan kod yığını
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
ch = "3"
while True:
    wss+=1
    if wss == 1:
       print("calibration")
       dalay.calibration()
    else:
        if ch == "1":
            dalay.stop()
            dalay.stopup()
            dalay.wait()
            time.sleep(2)
            dalay.down(2)
            dalay.sabit(2)
            time.sleep(5)
            dalay.stopup()
            dalay.stop()
            dalay.forward(3)
            time.sleep(2)
            dalay.wait()
            dalay.backward(3)
            time.sleep(1)
        elif ch == "2":
            dalay.stop()
            dalay.stopup()
            dalay.wait()
            time.sleep(2)
            dalay.down(2)
            dalay.sabit(2)
            time.sleep(5)
            dalay.stopup()
            dalay.stop()
            dalay.forward(8)
            time.sleep(6)
        elif ch == "3":
            dalay.stop()
            dalay.stopup()
            dalay.wait()
            time.sleep(2)
            dalay.down(8)
            dalay.turnleft(8)
            time.sleep(10)
            
        elif ch == "4":
            pass

        elif ch == "8":
            dalay.stop()
            dalay.stopup()
            dalay.wait()
            time.sleep(3)
            dalay.down(2)
            dalay.sabit(2)
            time.sleep(3)
            dalay.wait()
            dalay.stopup()
            dalay.forward(4)
            time.sleep(5)
            dalay.stop()
            dalay.stopup()
        elif ch == "9":
            dalay.stop()
            dalay.stopup()
            dalay.wait()
            time.sleep(3)
            dalay.down(2)
            dalay.sabit(2)
            time.sleep(3)
            dalay.wait()
            dalay.stopup()
            dalay.left(2)
            time.sleep(5)
            dalay.right(2)
            time.sleep(5)
            dalay.stop()
            dalay.stopup()
        elif ch == "10":
            dalay.stop()
            dalay.stopup()
            dalay.wait()
            time.sleep(3)
            dalay.down(2)
            dalay.sabit(2)
            time.sleep(3)
            dalay.wait()
            dalay.stopup()
            dalay.turnleft(2)
            time.sleep(2)
            dalay.wait()
            time.sleep(2)
            dalay.turnright(2)
            time.sleep(3)
            dalay.wait()
            time.sleep(2)
            dalay.forward(2)
            time.sleep(6)
            dalay.stop()
            dalay.stopup()





