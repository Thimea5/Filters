import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

###### FONCTIONNE POUR AJOUTER LES LUNETTES SUR LES YEUX



def getWebcamVideo():
    #On initialise le flux de la capture vidéo
    videoWebcam = cv.VideoCapture(0)

    #On fait une boucle infinie pour faire la capture en temps réel
    while True:
        returnValue, webcamImage = videoWebcam.read()
        faces = face_cascade.detectMultiScale(webcamImage, 1.1, 4)
        for (x, y, w, h) in faces:
            eyes = eye_cascade.detectMultiScale(webcamImage[y:y+h, x:x+w])
            if len(eyes) >= 2:  # Check if both eyes are detected
                # Use the position of the first detected eye to place sunglasses
                ex1, ey1, ew1, eh1 = eyes[0]
                x_pos = x + ex1
                y_pos = y + ey1

                # Use the distance between the eyes to resize sunglasses
                eye_distance = eyes[1][0] - eyes[0][0] + eyes[1][2]
                resize_factor = eye_distance / sunglasses.shape[1]

                # Ensure that resize_factor is positive before resizing
                if resize_factor > 0:
                # Resize sunglasses
                    resized_sunglasses = cv.resize(sunglasses, (int(sunglasses.shape[1] * resize_factor), int(sunglasses.shape[0] * resize_factor)))

                    # Ensure that the sunglasses do not go out of bounds
                    y_start, y_end = max(y_pos, 0), min(y_pos + resized_sunglasses.shape[0], webcamImage.shape[0])
                    x_start, x_end = max(x_pos, 0), min(x_pos + resized_sunglasses.shape[1], webcamImage.shape[1])

                    # Overlay sunglasses on the frame
                    mask = resized_sunglasses[:, :, 3] / 255.0
                    for c in range(3):
                        webcamImage[y_start:y_end, x_start:x_end, c] = (
                            webcamImage[y_start:y_end, x_start:x_end, c] * (1 - mask) +
                            resized_sunglasses[:, :, c] * mask
                        )
    
   
    # Display
        cv.imshow('webcam', webcamImage)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    videoWebcam = cv.VideoCapture.release()
    cv.destroyAllWindows()

# Load the cascade
face_cascade = cv.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
eye_cascade = cv.CascadeClassifier('./haarcascades/haarcascade_eye_tree_eyeglasses.xml')

sunglasses = cv.imread('./images/sunglasses.png', cv.IMREAD_UNCHANGED)

getWebcamVideo()