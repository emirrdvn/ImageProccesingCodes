import cv2
import time

def __gstreamer_pipeline(
        camera_id,
        capture_width=1920,
        capture_height=1080,
        display_width=1920,
        display_height=1080,
        framerate=30,
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
   
#cap = cv2.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=2), cv2.CAP_GSTREAMER)
#cap1 = cv2.VideoCapture(__gstreamer_pipeline(camera_id=1, flip_method=2), cv2.CAP_GSTREAMER)
# set up camera object
cap = cv2.VideoCapture(0)


# QR code detection object
prev_frame_time = 0
new_frame_time = 0

while True:
    # get the image
    _, img = cap.read()	
    #_, img1 = cap1.read()
#resized code
    scale_percent = 50
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    # width1 = int(img1.shape[1] * scale_percent / 100)
    # height1 = int(img1.shape[0] * scale_percent / 100)
    dim = (width, height) 
    #dim1 = (width, height) 
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    #resized1 = cv2.resize(img1, dim1, interpolation = cv2.INTER_AREA)
	###### FPS SHOW
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
    cv2.putText(resized, fps, (7, 70), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
    #cv2.putText(resized1, fps, (7, 70), font, 3, (0, 255, 0), 3, cv2.LINE_AA)
    shapes = img.shape

    #cv2.imshow("kk2", resized1)
    cv2.imshow("kk1",resized)
    if(cv2.waitKey(1) == ord("q")):
        break
# free camera object and exit
cap.release()
cv2.destroyAllWindows()
