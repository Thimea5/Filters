import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def getWebcamVideo():
    #On initialise le flux de la capture vidéo
    videoWebcam = cv.VideoCapture(0)

    #On fait une boucle infinie pour faire la capture en temps réel
    while True:
        returnValue, webcamImage = videoWebcam.read()
        faces = face_cascade.detectMultiScale(webcamImage, 1.1, 4)
        for i in faces:
            eye = eye_cascade.detectMultiScale(webcamImage, 1.1, 4)
            for a,b,c,d in eye:
                webcamImage = cv.ellipse(webcamImage, (a + int(c*0.5), b + int(d*0.5)),(int(c*0.5),int(d*0.5)), 0,0,360,(255, 0, 255), 4)
   
    # Display
        cv.imshow('webcam', webcamImage)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    videoWebcam = cv.VideoCapture.release()
    cv.destroyAllWindows()

# Load the cascade
face_cascade = cv.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
eye_cascade = cv.CascadeClassifier('./haarcascades/haarcascade_eye_tree_eyeglasses.xml')

sunglasses = cv.imread('./images/sunglasses.png') 

getWebcamVideo()