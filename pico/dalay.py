from machine import Pin,PWM
import time
class dalay:
    #6 tane motor için pin girdisi
    def __init__(self,freq,pwm0,pwm1,pwm2,pwm3,pwm4,pwm5):
            self.freq = freq
            self.pwm0 = Pin(pwm0)#onmotor1
            self.pwm1 = Pin(pwm1)#onmotor2
            self.pwm2 = Pin(pwm2)#arkamotor1
            self.pwm3 = Pin(pwm3)#arkamotor2
            self.pwm4 = Pin(pwm4)#ustmotor1
            self.pwm5 = Pin(pwm5)#ustmotor2
            #1->sag 2->sol
    #motor için kalibrasyon girdisi
    #dutycycle 13655 21
    #dutycycle sidemin 20.6
    #dutycycle sidemax 18.6
    #dutycycle backmin 21.4
    #dutycycle backmax 23.3
    def calibration(self):
        pwmOutput0 = PWM(self.pwm0)
        pwmOutput1 = PWM(self.pwm1)
        pwmOutput2 = PWM(self.pwm2)
        pwmOutput3 = PWM(self.pwm3)
        pwmOutput4 = PWM(self.pwm4)
        pwmOutput5 = PWM(self.pwm5)
        pwmOutput0.freq(int(self.freq))
        pwmOutput1.freq(int(self.freq))
        pwmOutput2.freq(int(self.freq))
        pwmOutput3.freq(int(self.freq))
        pwmOutput4.freq(int(self.freq))
        pwmOutput5.freq(int(self.freq))
        self.stop()

    #pwm sinyalinin hıza dönüştürüldüğü fonskiyon
    #1000-2000 arası
    #1000-1500
    #1500-2000 arası speed ayarla
    def speed(self,speed):
        cspeedmin = 1000
        cminpwm = 20.6
        
        cspeedmax = 1499
        cmaxpwm = 18.6

        #cstop = 1500
        cxstop = 21

        cxminpwm = 21.4
        cxspeedmin = 1501

        cxmaxpwm = 23.4
        cxspeedmax = 2000
        if 999<speed<1500:
            cpwmSpan = cmaxpwm-cminpwm
            cSpan = cspeedmax-cspeedmin
            vScaled = float(speed - cspeedmin) / float(cSpan)
            return round(cminpwm+(vScaled*cpwmSpan),2)
        elif 1500<speed<2001:
            cxpwmSpan = cxmaxpwm-cxminpwm
            cxSpan = cxspeedmax-cxspeedmin
            vScaled = float(speed - cxspeedmax) / float(cxSpan)
            return round(cxmaxpwm+(vScaled*cxpwmSpan),2)
        else:
            return cxstop
    def duty_cycle(self,sp):
        return int(self.speed(sp) * 65025 / 100)
    #----------------PID--------------------#
    def forward_control(self,error,direction):#direction:~1->left|0->right~
        if direction:
            PWM(self.pwm0).duty_u16(self.duty_cycle(1100+error))
            PWM(self.pwm1).duty_u16(self.duty_cycle(1100))
            PWM(self.pwm2).duty_u16(self.duty_cycle(1600+error))
            PWM(self.pwm3).duty_u16(self.duty_cycle(1600))
        else:
            PWM(self.pwm0).duty_u16(self.duty_cycle(1100))
            PWM(self.pwm1).duty_u16(self.duty_cycle(1100+error))
            PWM(self.pwm2).duty_u16(self.duty_cycle(1600))
            PWM(self.pwm3).duty_u16(self.duty_cycle(1600+error))
    #/---------------------------------------/
    def turnright(self,level=3):#default 2
        self.control(0,level,1)
        self.control(1,level,0)
        self.control(2,level,0)
        self.control(3,level,1)
    def turnleft(self,level=3):#default 2
        self.control(0,level,0)
        self.control(1,level,1)
        self.control(2,level,1)
        self.control(3,level,0)
    def backward(self,level=3):#default 4
        self.control(0,level,1)#pin,kademe,yön
        self.control(1,level,1)
        self.control(2,level,0)
        self.control(3,level,0)
    def forward(self,level=3):
        self.control(0,level,0)
        self.control(1,level,0)
        self.control(2,level,1)
        self.control(3,level,1)
    def stop(self):
        PWM(self.pwm0).duty_u16(self.duty_cycle(1500))
        PWM(self.pwm1).duty_u16(self.duty_cycle(1500))
        PWM(self.pwm2).duty_u16(self.duty_cycle(1500))
        PWM(self.pwm3).duty_u16(self.duty_cycle(1500))
    def stopup(self):
        PWM(self.pwm4).duty_u16(self.duty_cycle(1500))
        PWM(self.pwm5).duty_u16(self.duty_cycle(1500))
    def up(self,level=4):
        self.control(4,level,0)
    def down(self,level=4):
        self.control(4,level,1)
    def wait(self):
        self.stop()
        time.sleep(0.2)
    def left(self,level=3):
        self.control(0,level,0)
        self.control(1,level,1)
        self.control(2,level,0)
        self.control(3,level,1)
    def right(self,level=3):
        self.control(0,level,1)
        self.control(1,level,0)
        self.control(2,level,1)
        self.control(3,level,0)
    def sabit(self,level=3):
        self.control(0,level,1)#pin,kademe,yön
        self.control(1,level,1)
        self.control(2,level,1)
        self.control(3,level,1)
        self.control(4,level,1)
        self.control(5,level,1)
    def test(self,level=3):
        self.control(0,level,1)#pin,kademe,yön
        self.control(1,level,1)#pin,kademe,yön
        self.control(2,level,1)#pin,kademe,yön
        self.control(3,level,1)#pin,kademe,yön
        
    def run(self,pwm,speed):
        pwmselector = { 
            0:Pin(self.pwm0),
            1:Pin(self.pwm1),
            2:Pin(self.pwm2),
            3:Pin(self.pwm3),
            4:Pin(self.pwm4),
            5:Pin(self.pwm5)
        }
        PWM(Pin(pwmselector.get(pwm,"nothing"))).duty_u16(self.duty_cycle(speed))
    def rightLeftSelector(self,selectoption):
        options = {
                1:(self.duty_cycle(1000),self.duty_cycle(1502)),#1
                2:(self.duty_cycle(1050),self.duty_cycle(1550)),#1.5
                3:(self.duty_cycle(1100),self.duty_cycle(1600)),#2
                4:(self.duty_cycle(1150),self.duty_cycle(1650)),#2.5
                5:(self.duty_cycle(1200),self.duty_cycle(1700)),#3
                6:(self.duty_cycle(1250),self.duty_cycle(1750)),#3.5
                7:(self.duty_cycle(1300),self.duty_cycle(1800)),#4
                8:(self.duty_cycle(1350),self.duty_cycle(1850)),#4.5
                9:(self.duty_cycle(1400),self.duty_cycle(1900)),#5
                10:(self.duty_cycle(1450),self.duty_cycle(1950)),#5.5
                11:(self.duty_cycle(1499),self.duty_cycle(2000))#6
                
            }
        return options.get(selectoption,"nothing")     
        
    def control(self,pwm,option,rl):#pin,kademe,yön
        pwmselector = {
            0:self.pwm0,
            1:self.pwm1,
            2:self.pwm2,
            3:self.pwm3,
            4:self.pwm4,
            5:self.pwm5
        }
        PWM(pwmselector.get(pwm,"nothing")).duty_u16(self.rightLeftSelector(option)[rl])         
        


