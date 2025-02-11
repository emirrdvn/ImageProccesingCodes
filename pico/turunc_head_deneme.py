#### görüntü işleme kodları ile hedef saptanmadan önce düz gitmesini sağlayan algoritma ile görüntü işleme kodlarının birleştirilme denemesi(Test edilmedi) made by Samet
from dalay import dalay
import select
import sys
import machine
import utime
import time
from bno055_base import BNO055_BASE
from machine import Pin
dalay = dalay(50,0,11,12,19,4,20)#pinleri belirt 50 freq digerleri 0,1,2,3,4,5 pin
led = Pin(25, Pin.OUT)
wss=0
ch =""
c=""
komut=""
def conversion(x,f_head):
    if x>=f_head:
        return x-f_head
    else:
        return x+360-f_head
i2c = machine.I2C(0,sda=machine.Pin(8), scl=machine.Pin(9),freq=4000)
imu = BNO055_BASE(i2c)
calibrated = False
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
        if select.select([sys.stdin],[],[],0)[0]:
            ch1 = sys.stdin.readline()
            ch1=ch1.strip()
            print(ch1)
            heuler=conversion(imu.euler()[0],f_imu)
            print(heuler)
            if(40>heuler>2):
                komut="sol"
            elif(358>heuler>340):
                komut="sag"
            else:
                komut="ileri"
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
 
        
 
 




