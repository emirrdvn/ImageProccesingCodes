from dalay import dalay
import time
from machine import Pin

dalay = dalay(50,0,11,12,19,4,16)#pinleri belirt 50 freq digerleri 0,1,2,3,4,5 pin
led = machine.Pin(25,Pin.OUT)
led.high()
time.sleep(0.5)
led.low()
time.sleep(0.5)
led.high()
wss=0
while True:
        wss+=1
        if wss == 1:
            print("calibration")
            dalay.calibration()
        else:
            print("Başlıyoruz.")
            dalay.wait()
            time.sleep(1)
            dalay.xx(0,1)
            dalay.xx(1,1)
            dalay.xx(2,1)
            dalay.xx(3,1)
            dalay.xx(4,1)
            dalay.xx(5,1)
            time.sleep(5)
            dalay.stop()