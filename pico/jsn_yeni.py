###jsn 
from machine import Pin
import time

def distance1(trig,echo,sira):
          trig = Pin(trig, Pin.OUT)
          echo = Pin(echo, Pin.IN, Pin.PULL_DOWN)
          trig.value(0)
          time.sleep(0.1)
          trig.value(1)
          time.sleep_us(2)
          trig.value(0)
          while echo.value()==0:
               pulse_start = time.ticks_us()
          while echo.value()==1:
               pulse_end = time.ticks_us()
          pulse_duration = pulse_end - pulse_start
          distance = pulse_duration * 17165 / 1000000
          distance = round(distance, 0)
          return print ('Distance{}:'.format(sira),"{:.0f}".format(distance),'cm')
while True:
    distance1(11,10,2)
    #distance1(13,14,1)
    