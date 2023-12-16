import numpy as np
import cv2 as cv
cap = cv.VideoCapture('./TD5/images/video2.avi')

width = cap.get(cv.CAP_PROP_FRAME_WIDTH);
n = 6;
delta = int(width/n); #divide image in n parts

while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
  
    #pass from RGB to graylevel
    p1 = frame[0:frame.shape[0],delta:frame.shape[1]];
    p1_gray = cv.cvtColor(p1, cv.COLOR_BGR2GRAY)
    p1 = cv.cvtColor(p1_gray, cv.COLOR_GRAY2BGR)
    
    #copy processed part to frame
    frame[0:frame.shape[0],delta:frame.shape[1]] = p1
    
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()