from machine import Pin, I2C
import utime
trigger1 = Pin(5, Pin.OUT)
echo1 = Pin(4, Pin.IN)
trigger2 = Pin(7, Pin.OUT)
echo2 = Pin(6, Pin.IN)
trigger3 = Pin(10, Pin.OUT)
echo3 = Pin(11, Pin.IN)
trigger4 = Pin(13, Pin.OUT)
echo4 = Pin(14, Pin.IN)
def xd(timepassed):
    measured_time = timepassed     
    distance_cm = (measured_time * 0.0343) / 2
    distance_cm = round(distance_cm,2)
    return distance_cm
while True:
    timepassed=0
    trigger1.low()
    trigger2.low()
    trigger3.low()
    trigger4.low()
    utime.sleep_us(2)
    trigger1.high()
    trigger2.high()
    trigger3.high()
    trigger4.high()
    utime.sleep_us(5)
    trigger1.low()
    trigger2.low()
    trigger3.low()
    trigger4.low()
    while echo1.value() == 0:
        signaloff1 = utime.ticks_us()
        signaloff2 = utime.ticks_us()
        signaloff3 = utime.ticks_us()
        signaloff4 = utime.ticks_us()
    while echo1.value() == 1:
        signalon1 = utime.ticks_us()
        signalon2 = utime.ticks_us()
        signalon3 = utime.ticks_us()
        signalon4 = utime.ticks_us()
    timepassed1 = signalon1 - signaloff1
    timepassed2 = signalon2 - signaloff2
    timepassed3 = signalon3 - signaloff3
    timepassed4 = signalon4 - signaloff4
    
    print(xd(timepassed1))
    print(xd(timepassed2))
    print(xd(timepassed3))
    print(xd(timepassed4))
    utime.sleep(1)