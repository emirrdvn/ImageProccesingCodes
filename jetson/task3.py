from configparser import Interpolation
from ctypes import resize
import numpy as np
import cv2
import time  
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
webcam = cv2.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=2), cv2.CAP_GSTREAMER)
webcam1 = cv2.VideoCapture(__gstreamer_pipeline(camera_id=1, flip_method=2), cv2.CAP_GSTREAMER)
#webcam = cv2.VideoCapture(0)
#webcam1 = cv2.VideoCapture("havuzvid1.mp4")

prev_frame_time = 0
new_frame_time = 0  
area_border = 500
width = 640
height = 480
cam_height = 480
cam_width = 640
merkez_uzaklik = 50
merkez_uzaklik = 50
# Start a while loop

dim = (width,height)

while(1):
    durum="None"
    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()
    _, imageFrame1 = webcam1.read()
    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
    # Set range for blue color and 
    # define mask
    blue_lower = np.array([99, 100, 100], np.uint8)
    blue_upper = np.array([101, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
    
    # blue_lower = np.array([100, 50, 38], np.uint8)
    # blue_upper = np.array([120, 255, 255], np.uint8)
    # blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)#
    # Set range for green color and 
    # define mask
    green_lower = np.array([50, 100, 100], np.uint8)
    green_upper = np.array([80, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    #hsv output

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")
      
    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
                              mask = blue_mask)
      
    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                mask = green_mask)

    green_Blue = blue_mask+green_mask
    res = cv2.bitwise_and(imageFrame,imageFrame ,mask=green_Blue)

    # Creating contour to track blue color
    blue_contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    # Creating contour to track green color
    green_contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(imageFrame, (0, int(height / 2)), (int(width), int(height / 2)), (255, 0, 0), 1)
    cv2.line(imageFrame, (int(width / 2), 0), (int(width / 2), int(height)), (0, 0, 0), 1)
    cv2.rectangle(imageFrame, (int(cam_width / 2 - merkez_uzaklik), int(cam_height / 2 - merkez_uzaklik)),
                  (int(cam_width / 2 + merkez_uzaklik), int(cam_height / 2 + merkez_uzaklik)), (0, 255, 0),
                  2)  # true location

    cv2.rectangle(imageFrame, (int(cam_width / 2 - merkez_uzaklik), int(0)),
                  (int(cam_width / 2 + merkez_uzaklik), int(cam_height / 2 - merkez_uzaklik)), (255, 0, 255),
                  2)  # ust ortalama kontrol
    cv2.rectangle(imageFrame, (int(cam_width / 2 - merkez_uzaklik), int(cam_height)),
                  (int(cam_width / 2 + merkez_uzaklik), int(cam_height / 2 + merkez_uzaklik)), (255, 0, 255),
                  2)  # alt ortalama kontrol

    #area1 = cv2.contourArea(contour)#took contours one by one
    #green algilama
    area1 = [cv2.contourArea(c) for c in green_contours]#took all the contours to the area1

    if len(area1) == 0:#kotu kontrol durumu
        area1.append(0)
        green_contours = green_contours + [0,]

    print("area green:"+str(area1))
    area1_maxindex=np.argmax(area1)#biggest area on area1
    cnt=green_contours[area1_maxindex]
    enbuyukgreen=area1[area1_maxindex]
    print("this is biggest green area:" + str(enbuyukgreen))
    #print("this is biggest green cnt:" + str(cnt))


    # blue algilama
    area2 = [cv2.contourArea(c1) for c1 in blue_contours]  # took all the contours to the area2

    if len(area2) == 0:  # kotu kontrol durumu
        area2.append(0)
        blue_contours = blue_contours + [0,]

    print("area blue:" + str(area2))
    area2_maxindex = np.argmax(area2)  # biggest area on area2
    cnt1 = blue_contours[area2_maxindex]
    enbuyuk_blue = area2[area2_maxindex]
    print("this is biggest blue area:" + str(enbuyuk_blue))
    #print("this is biggest blue cnt1:" + str(cnt1))


    if(enbuyukgreen > area_border+100 and enbuyuk_blue > area_border+100):
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                       (x + w, y + h), 
                                       (0, 255, 0), 2)
            cv2.putText(imageFrame, str(enbuyukgreen), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 255, 255))

            i = [int(x + w / 2), int(y + h / 2), int(h / 2)]  # green radius coordinates and radius=x,y,radius




            if(True) :# ???
                    peri1 = cv2.arcLength(cnt1, True)
                    approx1 = cv2.approxPolyDP(cnt1, 0.01 * peri1, True)
                    x1, y1, w1, h1 = cv2.boundingRect(approx1)
                    imageFrame = cv2.rectangle(imageFrame, (x1, y1),
                                            (x1 + w1, y1 + h1),
                                            (0, 0, 255), 2)

                    cv2.putText(imageFrame, str(enbuyuk_blue), (x1, y1),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (0, 255, 255))
                    cv2.line(imageFrame, (int(x + w / 2), int(y + h / 2)), (int(x1 + w1 / 2), int(y1 + h1 / 2)), (212, 121, 255), 5)  # x

                    icenter = [int(((x + w / 2) + (x1 + w1 / 2)) / 2), int(((y + h / 2) + (y1 + h1 / 2)) / 2),
                               3]  # yesil ve kirmizinin orta noktasinin koordinatlarini ve yaricapini tutar

                    cv2.line(imageFrame, (int(x + w / 2), int(y + h / 2)), (int(x1 + w1 / 2), int(y1 + h1 / 2)),
                             (212, 121, 255), 10)  # connect two orange circles
                    cv2.circle(imageFrame, (int(((x + w / 2) + (x1 + w1 / 2)) / 2), int(((y + h / 2) + (y1 + h1 / 2)) / 2)),
                               (3), (212, 121, 0), 10)  # orta noktayi gostermek icin bir nokta
                    print("orta nokta kordinatlari:" + str(
                        (int(((x + w / 2) + (x1 + w1 / 2)) / 2), int(((y + h / 2) + (y1 + h1 / 2)) / 2))))

                    temp = 1
                    if temp == 1:
                        # if((len(approx) > 8) & (len(approx) < 23) & (area > 30))://daire bulucu sorgu
                        cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0),
                                      3)  # en buyuk bulunan sekil kare icine alma
                        cv2.rectangle(imageFrame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0),
                                      3)  # ikinci en buyuk bulunan sekil kare icine alma
                        # cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 3)#en buyuk bulunan sekil daire icine alma

                        ##en buyuk olan sekil icin hipotenus,x ve y cizgileri
                        # cv2.line(img, (320, 240), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)  # hipotenus
                        # cv2.line(img, (int(x + w / 2), int(y + h / 2)), (320, int(y + h / 2)), (0, 0, 255), 1)  # x
                        # cv2.line(img, (int(x + w / 2), int(y + h / 2)), (int(x + w / 2), 240), (0, 0, 255), 1)  # y
                        # cv2.rectangle(img, (x - 5, y - 5), (x + 5,y + 5), (0, 128, 255), -1)
                        # cv2.line(img, (int(width / 2), int(height / 2)), (x, y), (0, 255, 0), 2)

                        # yonelim algoritmasi icin
                        cv2.line(imageFrame, (0, int(cam_height / 2)), (int(cam_width), int(cam_height / 2)), (255, 0, 0), 1)
                        cv2.line(imageFrame, (int(cam_width / 2), 0), (int(cam_width / 2), int(cam_height)), (0, 0, 0), 1)

                        a = icenter[0] - cam_width / 2
                        b = cam_height / 2 - icenter[1]

                        # print("x'in uzakligi:",i[0],"y'nin uzakligi:",i[1])
                        # cv2.putText(img, "ust ortalama x={}  y={}".format(i[0], i[1]), (800, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        #                                 .8, (0, 255, 0), 3, cv2.LINE_AA)
                        if (int(cam_width / 2 + merkez_uzaklik) > icenter[0] > int(
                                cam_width / 2 - merkez_uzaklik) and int(
                                cam_height / 2 - merkez_uzaklik) > icenter[1] > int(0)):
                            durum = "ust ortalama"
                            print("ust ortalama")

                        elif (int(cam_width / 2 + merkez_uzaklik) > icenter[0] > int(
                                cam_width / 2 - merkez_uzaklik) and int(cam_height) > icenter[
                                  1] > int(cam_height / 2 + merkez_uzaklik)):
                            durum = "alt ortalama"
                            print("alt ortalama")

                        elif (int(cam_width / 2 + merkez_uzaklik) > icenter[0] > int(
                                cam_width / 2 - merkez_uzaklik) and int(
                                cam_height / 2 + merkez_uzaklik) > icenter[1] > int(cam_height / 2 - merkez_uzaklik)):
                            durum = "ortalama"
                            print("ortalama")

                        elif (a > 0 and b > 0):
                            durum = "sag ust"
                            print("sag ust")

                        elif (a > 0 and b < 0):
                            durum = "sag alt"
                            print("sag alt")

                        elif (a < 0 and b > 0):
                            durum = "sol ust"
                            print("sol ust")

                        else:
                            durum = "sol alt"
                            print("sol alt")
    print("durum:" + durum)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()

    # Calculating the fps

    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # converting the fps into integer
    fps = int(fps)

    # converting the fps to string so that we can display it on frame
    # by using putText function
    fps = str(fps)

    # putting the FPS count on the frame
    cv2.putText(imageFrame, fps, (7, 70), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(imageFrame1, fps, (7, 70), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    cv2.imshow("2. gamera",imageFrame1)
    cv2.imshow("res",res)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break