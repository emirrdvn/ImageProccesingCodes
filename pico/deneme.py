import sys
import time

#for i in range(1,16):
#    print(sys.stdout.write(str(i)))
#    time.sleep(1)
import machine
import time
from bno055_base import BNO055_BASE

i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8))
imu = BNO055_BASE(i2c)
calibrated = False
a,b,c=0,0,0
while True:
    time.sleep(0.5)
    if not calibrated:
        calibrated = imu.calibrated()
        #print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
    #print('sıcaklık {}°C'.format(imu.temperature()))
    #print('Mıknatıslanma       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
    #print('jiroskop                x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
    #print('ivme                x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
    #print('hızlanma vektoru    x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
    #print('yer çekimi ivmesi   x {:5.1f}    y {:5.1f}     z {:5.6f}'.format(*imu.gravity()))#+
    
    #print('Heading  {:4.1f} roll {:4.1f} pitch {:4.1f}'.format(*imu.euler()))
    print(sys.stdout.write('{:4.1f},{:4.1f},{:4.1f}'.format(*imu.euler())))
    time.sleep(1)
    #d,e,f=imu.lin_acc()
    #print(d-a,e-b,f-c)
    #a,b,c=d,e,f
    
    
    
    