import cv2
import numpy as np
import math
import sys
import select
import serial
import os
from datetime import datetime

#ser = serial.Serial('/dev/ttyACM0') #for linux/
#ser = serial.Serial('COM10') #For windows 

# Capturing Video through webcam.
def nothing(x):
    # any operation
    pass

def resize_dim(img,scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return dim

def secondlargest(arr,arr_size):
    # There should be
    # atleast three elements
    if (arr_size < 2):
        print(" Invalid Input ")
        return
    # Find first
    # largest element
    first = arr[0]
    for i in range(1, arr_size):
        if (arr[i] > first):
            first = arr[i]
    # Find second
    # largest element
    second = -sys.maxsize
    secin=0
    for i in range(0, arr_size):
        if (arr[i] > second and arr[i] < first):
            second = arr[i]
            secin=i
    return secin
def __gstreamer_pipeline(
        camera_id,
        capture_width=640,
        capture_height=480,
        display_width=640,
        display_height=480,
        framerate=60,
        flip_method=0,
    ):
    return (
            "nvarguscamerasrc sensor-id=%d ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
            % (
                    camera_id,
                    capture_width,
                    capture_height,
                    framerate,
                    flip_method,
                    display_width,
                    display_height,
            )
    )
#Get frame 
video = cv2.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=2), cv2.CAP_GSTREAMER)
#video = cv2.VideoCapture(0)
#width = video.get(cv2.CAP_PROP_FRAME_WIDTH)  # 640
#height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 480
#Dimention definition
width = 640
height = 480
cam_height = 480
cam_width = 640

#save files directory
try:
    os.mkdir("saved_videos")
except OSError as error:
    print(error)

now = datetime.now()
date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
os.mkdir("saved_videos/"+date_time)
result = cv2.VideoWriter("saved_videos/"+date_time+"/result--"+date_time+".mov", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
input_frame = cv2.VideoWriter("saved_videos/"+date_time+"/inp--"+date_time+".mov", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

while (1):
    _, img = video.read()
    img=np.fliplr(img)#ayna etkisi
    img = cv2.resize(img, (width,height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    img1 = img.copy()
    # converting frame(img) from BGR (Blue-Green-Red) to HSV (hue-saturation-value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # defining the range of different colors
    # yellow_lower = np.array([22, 100, 100], np.uint8)
    # yellow_upper = np.array([60, 255, 255], np.uint8)
    green_lower = np.array([38, 85, 0], np.uint8)
    green_upper = np.array([90, 255, 255], np.uint8)
    blue_lower = np.array([101, 50, 38], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)
    red_lower = np.array([160, 110, 70], np.uint8)  # abwater red=160, 20, 70                underwater red=0,0,0
    red_upper = np.array([190, 255, 255], np.uint8)  # abwater red=190, 255, 255             underwater red=190, 100, 220
    yellow_lower = np.array([22, 93, 0], np.uint8)
    yellow_upper = np.array([27, 255, 255], np.uint8)
    orange_lower = np.array([0,100,100], np.uint8)
    orange_upper = np.array([10, 250, 255], np.uint8)
    black_lower = np.array([0,0,0], np.uint8)
    black_upper = np.array([180, 255, 50], np.uint8)
    # finding the range of colours in the image
    green = cv2.inRange(hsv, green_lower, green_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    red = cv2.inRange(hsv, red_lower, red_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    orange = cv2.inRange(hsv, orange_lower, orange_upper)
    black = cv2.inRange(hsv, black_lower, black_upper)

    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")

    blue = cv2.dilate(blue, kernal)

    res = cv2.bitwise_and(img, img, mask=orange)
    #middle lines
    cv2.line(img, (0, int(height / 2)), (int(width), int(height / 2)), (0, 0, 255), 1)
    cv2.line(img, (int(width / 2), 0), (int(width / 2), int(height)), (0, 0, 255), 1)

    # Tracking Colour (yellow)
    (contours, _) = cv2.findContours(orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    center_distance = 50
    cv2.rectangle(img, (int(cam_width / 2 - center_distance), int(cam_height / 2 - center_distance)),
                  (int(cam_width / 2 + center_distance), int(cam_height / 2 + center_distance)), (0, 255, 0),
                  2)  # true location

    cv2.rectangle(img, (int(cam_width / 2 - center_distance), int(0)),
                  (int(cam_width / 2 + center_distance), int(cam_height / 2 - center_distance)), (255, 0, 255),
                  2)  # ust ortalama kontrol
    cv2.rectangle(img, (int(cam_width / 2 - center_distance), int(cam_height)),
                  (int(cam_width / 2 + center_distance), int(cam_height / 2 + center_distance)), (255, 0, 255),
                  2)  # alt ortalama kontrol

    # en buyuk olan contour secme islemi
    area = [cv2.contourArea(c) for c in contours]  # butun bulunan contourlar area sinifina atiliyor
    areacopy=area.copy()
    areacopy.sort()
    areacopy.reverse()
    #print("this is area:" + str(area))  # butun contourlarin alanini yazdirir
    #print("buyukten kucuge:"+ str(areacopy))

    durum = "None"
    if len(area) == 0 or len(area)==1:  # eger area listesinin boyutu 0 ise program patlamamasi icin o adimi atlatiyoruz
        area.append(0)
        area.append(1)
        contours=contours+[0,]
        contours=contours+[1,]
        #ser.write(f"{durum}\n".encode("utf-8")) #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONT FORGET TO CHANGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    max_index = np.argmax(area)  # the biggest index number
    second_index = secondlargest(area,len(area))
    #max_index = len(area)-1#sort ile siralandigi icin en son deger en buyuk degerdir
    #second_index= len(area)-2#en buyuk 2. yi bulma
    # print("bu max index:"+str(max_index))
    # print("second index:"+str(second_index))
    # print("biggest index:" + str(max_index))
    cnt=contours[max_index]
    cnt1 = contours[second_index]

    deneme = area[max_index]  # max index
    deneme1 = area[second_index]
    print("this is biggest area:" + str(deneme))  # en buyuk contour'un alanini yazdirir
    print("this is second biggest area:" + str(deneme1))

    if (deneme1>200):##minimum kabul edilebilir sekil boyutu
        ###en buyuk olan turuncu icin
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)  # get borders locations
        objcor = len(approx) #get number of edges
        x, y, w, h = cv2.boundingRect(approx)

        i = [int(x + w / 2), int(y + h / 2), int(h / 2)]  # circle coordinates and radius=x,y,radius
        # for radius h/2 or w/2

        ###en buyukten bir kucuk olan turuncu icin
        peri1 = cv2.arcLength(cnt1, True)
        # print(peri)
        approx1 = cv2.approxPolyDP(cnt1, 0.01 * peri1, True)  # algilanan kenarlarin lokasyonunu tutar
        # print(approx)
        # print(len(approx))#sekillerin kenar sayisini soyler 3 ucgen 4 kare 4 den fazla ise daire elde etmis oluruz
        objcor1 = len(approx1)
        x1, y1, w1, h1 = cv2.boundingRect(approx1)

        i1 = [int(x1 + w1 / 2), int(y1 + h1 / 2), int(h1 / 2)]  # circle radius coordinates and radius size=x,y,radius
        # for radius h/2 or w/2

        icenter = [int(((x+w/2)+(x1 + w1 / 2))/2), int(((y+h/2)+(y1 + h1 / 2))/2), 3]  # iki turuncunun orta noktasinin koordinatlarini ve yaricapini tutar

        cv2.line(img, (int(x + w / 2), int(y + h / 2)), (int(x1 + w1 / 2), int(y1 + h1 / 2)), (212, 121, 255), 10)  # connect two orange circles
        cv2.circle(img,(int(((x+w/2)+(x1 + w1 / 2))/2), int(((y+h/2)+(y1 + h1 / 2))/2)),(3),(212, 121, 0), 10) # orta noktayi gostermek icin bir nokta
        #print("orta nokta kordinatlari:"+str((int(((x+w/2)+(x1 + w1 / 2))/2), int(((y+h/2)+(y1 + h1 / 2))/2))))

        temp = 1
        if temp == 1:
            # if((len(approx) > 8) & (len(approx) < 23) & (area > 30))://daire bulucu sorgu
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)#en buyuk bulunan sekil kare icine alma
            cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 3)  #ikinci en buyuk bulunan sekil kare icine alma
            #cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 3)#en buyuk bulunan sekil daire icine alma

            # yonelim algoritmasi icin
            cv2.line(img, (0, int(cam_height / 2)), (int(cam_width), int(cam_height / 2)), (255, 0, 0), 1)
            cv2.line(img, (int(cam_width / 2), 0), (int(cam_width / 2), int(cam_height)), (0, 0, 0), 1)

            a = icenter[0] - cam_width / 2
            b = cam_height / 2 - icenter[1]


            # print("x'in uzakligi:",i[0],"y'nin uzakligi:",i[1])
            # cv2.putText(img, "ust ortalama x={}  y={}".format(i[0], i[1]), (800, 50), cv2.FONT_HERSHEY_SIMPLEX,
            #                                 .8, (0, 255, 0), 3, cv2.LINE_AA)
            if (int(cam_width / 2 + center_distance) > icenter[0] > int(cam_width / 2 - center_distance) and int(
                    cam_height / 2 - center_distance) > icenter[1] > int(0)):
                durum = "ust ortalama"
                print("ust ortalama")

            elif (int(cam_width / 2 + center_distance) > icenter[0] > int(cam_width / 2 - center_distance) and int(cam_height) > icenter[
                1] > int(cam_height / 2 + center_distance)):
                durum = "alt ortalama"
                print("alt ortalama")

            elif (int(cam_width / 2 + center_distance) > icenter[0] > int(cam_width / 2 - center_distance) and int(
                    cam_height / 2 + center_distance) > icenter[1] > int(cam_height / 2 - center_distance)):
                durum = "ortalama"
                print("ortalama")

            elif (a > 0 and b > 0):
                durum = "sag"#sag ust
                print("sag ust")

            elif (a > 0 and b < 0):
                durum = "sag"#sag alt
                print("sag alt")

            elif (a < 0 and b > 0):
                durum = "sol"#sol ust
                print("sol ust")

            else:
                durum = "sol"#sol alt
                print("sol alt")

            # cv2.rectangle(img,(x,y),(1,1),(255,0,0),1)
            
        # print(str(x) + "  " + str(y) + " " + str(w) + " " + str(h))

        #for saving as video

    #ser.write(f"{durum}\n".encode("utf-8"))
    print("durum:"+durum)
    result.write(img)
    input_frame.write(img1)
    cv2.imshow("Real frame", img)
    cv2.imshow("red res", res)
    #cv2.imshow("hsv", hsv)
    # cv2.imshow("green", green)
    # cv2.imshow("restotal", restotal)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        video.release()
        result.release()
        input_frame.release()
        cv2.destroyAllWindows()
        break

        # if (w * h < 10000):
        #    cv2.putText(img, "kucuk daire", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        # elif (w * h > 10000):
        #    cv2.putText(img, "buyuk daire", (x + w, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
        #                cv2.LINE_AA)


        #en buyuk ikinci degeri bulma
        #maximum = max(area[0], area[1])
        #second_max = min(area[0], area[1])
        #n = len(area)
        #for i in range(2, n):
        #    if area[i] > maximum:
        #        second_max = maximum
        #        maximum = area[i]
        #    else:
        #        if area[i] > second_max:
        #            second_max = area[i]