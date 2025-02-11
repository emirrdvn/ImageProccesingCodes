from machine import Pin
import time


trig = Pin(13,Pin.OUT)
echo = Pin(14,Pin.IN)
def find():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(5)
    trig.low()
    
    while echo.value() == 0:
        signaloff = time.ticks_us()
    while echo.value() == 1:
        signalon = time.ticks_us()
        
    timepassed = signalon - signaloff
    dist = (timepassed * 0.0343) / 2
    
    print("Distance is :",dist, "cm")
while True:
    find()
    time.sleep(1)
