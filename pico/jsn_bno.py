####long time no see uzun zaman önceki ghyro jsn birleştirme denemesi
from machine import Pin
import time
from bno055_base import BNO055_BASE

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
        
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8),freq=4000)
imu = BNO055_BASE(i2c)
calibrated = False
while True:
    time.sleep(0.5)
    if not calibrated:
        calibrated = imu.calibrated()
        #print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
        #print('sıcaklık {}°C'.format(imu.temperature()))-
        #print('Mıknatıslanma       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))-
        #print('jiroskop                x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
        #print('ivme                x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
        print('hızlanma vektoru    x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
        #print('yer çekimi ivmesi   x {:5.1f}    y {:5.1f}     z {:5.6f}'.format(*imu.gravity()))#denge için+
        #print("{:4.1f}".format(*imu.euler()))-
        #print("{:5.1f}".format(*imu.lin_acc()))-
        #utime.sleep(0.5)
    #print('Heading  {:4.1f} roll {:4.1f} pitch {:4.1f}'.format(*imu.euler()))
    #print('{:4.1f},{:4.1f},{:4.1f}'.format(*imu.euler()))
        distance1(11,10,2)
        #distance1(13,14,1)