import cv2
import numpy as np

def nothing(x):
    pass

video = cv2.VideoCapture(0)
cv2.namedWindow('image')
    # Create trackbars for color change
    # Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 180, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)

cv2.createTrackbar('HMax', 'image', 0, 188, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

while True:
    
    # Load image
    _, image = video.read()
    # Create a window
    frame = cv2.flip(image,1)

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')

    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    mask = cv2.inRange(hsv,lower,upper)

    cv2.imshow("original",frame)
    cv2.imshow("mask",mask)

    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
video.release()
