import cv2
import serial
import os
from datetime import datetime

video = cv2.VideoCapture(0)
width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)
try:
    os.mkdir("saved_videos")
except OSError as error:
    print(error)
now = datetime.now()
date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
os.mkdir("saved_videos/"+date_time)
result = cv2.VideoWriter("saved_videos/"+date_time+"/result--"+date_time+".avi", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
while (1):
    _, img = video.read()
    result.write(img)
    cv2.imshow("Real frame", img)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        video.release()
        result.release()
        cv2.destroyAllWindows()
        break