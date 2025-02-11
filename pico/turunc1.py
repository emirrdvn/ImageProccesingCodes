####qualificition gate'i algılayan görüntü işleme ve pico ile iletişim içeren kod.
from dalay import dalay
import select
import sys
import machine
import utime
import time         #time library for sleep
dalay = dalay(50,0,11,12,19,4,20)#pinleri belirt 50 freq digerleri 0,1,2,3,4,5 pin
from machine import Pin
led = Pin(25, Pin.OUT)
wss=0
ch =""
while True:
    wss+=1
    if wss == 1:
       print("calibration")
       dalay.calibration()
    else:
        if select.select([sys.stdin],[],[],0)[0]:
            ch1 = sys.stdin.readline()
            ch1=ch1.strip()
            print(ch1)
            if ch1 != ch:
                dalay.stopup()
                dalay.stop()
                dalay.wait()
                ch = ch1
                print("bekletildi")
            else:
                if ch not in {"ust ortalama","alt ortalama"}#dengeden sorumlu
                    dalay.up(1)
                if ch == "ust ortalama":
                    dalay.down(2)    
                elif ch == "alt ortalama":
                    dalay.up(2)    
                elif ch == "ortalama":
                    dalay.forward(1)
                    #if cıktıysa   
                elif ch == "sag":
                    dalay.turnright(1)
                elif ch == "sol":
                    dalay.turnleft(1)
                else:#none durumu
                    pass#algoritma kur
 
        
 
 



