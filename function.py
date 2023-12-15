import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk

# Param global :
closeWindow = False
activeSunglasses = False
activeHat = False

# Load the cascade
face_cascade = cv.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
eye_cascade = cv.CascadeClassifier('./haarcascades/haarcascade_eye_tree_eyeglasses.xml')
sunglasses = cv.imread('./images/sunglasses.png', cv.IMREAD_UNCHANGED)
hat = cv.imread('./images/hat.png', cv.IMREAD_UNCHANGED)

def tracer_rectangle(image, point1, point2, couleur=(0, 255, 0)):
    # Copier l'image pour éviter de modifier l'original
    img_rect = image.copy()
    # Tracer le rectangle à partir des deux points
    cv.rectangle(img_rect, point1, point2, couleur)
    return img_rect


def convert_image_for_tkinter(image):
    # Convertir l'image OpenCV en format RGB pour Tkinter
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # Convertir l'image en objet ImageTk pour Tkinter
    image = Image.fromarray(image)
    return ImageTk.PhotoImage(image)


def closeWindowF():
    global closeWindow
    closeWindow = True


def on_checkbox_checked_sunglasses(checkbox_var):
    global activeSunglasses
    if checkbox_var.get():
        activeSunglasses = True
    else:
        activeSunglasses = False


def on_checkbox_checked_hat(checkbox_var):
    global activeHat
    if checkbox_var.get():
        activeHat = True
    else:
        activeHat = False


def insideImg(webcamImage,point1,point2,img):
    resized_hat = cv.resize(img, (point2[0] - point1[0], point2[1] - point1[1])) 
    mask = resized_hat[:, :, 3] / 255.0
    for c in range(3):
        webcamImage[point1[1]:point2[1], point1[0]:point2[0], c] = (
        webcamImage[point1[1]:point2[1], point1[0]:point2[0], c] * (1 - mask) +
        resized_hat[:, :, c] * mask)
    return webcamImage

def getWebcamVideo(width, height):

    videoWebcam = cv.VideoCapture(0)
    point1 = (0,0)
    point2 = (0,0)

    # Créer une fenêtre Tkinter
    window = tk.Tk()
    window.protocol("WM_DELETE_WINDOW", closeWindowF)
    window.title("programme vidéo")
    
    # Création de la case à cocher
    checkbox_var_sunglasses = tk.BooleanVar()
    checkbox = tk.Checkbutton(window, text="Lunettes de soleil", variable=checkbox_var_sunglasses, command=lambda: on_checkbox_checked_sunglasses(checkbox_var_sunglasses))
    checkbox.pack(side="right",pady=0, padx=200)

    checkbox_var_hat = tk.BooleanVar()
    checkboxHat = tk.Checkbutton(window, text="Chapeau", variable=checkbox_var_hat, command=lambda: on_checkbox_checked_hat(checkbox_var_hat))
    checkboxHat.pack(side="right",pady=0, padx=100)

    # Créer un canevas Tkinter pour afficher l'image
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.pack()

    # On fait une boucle infinie pour faire la capture en temps réel
    while True:
        returnValue, webcamImage = videoWebcam.read()
        faces = face_cascade.detectMultiScale(webcamImage, 1.1, 4)

        for (xf,yf,wf,hf) in faces:
            i=0
            webcamImage = cv.ellipse(webcamImage, (xf + int(wf*0.5), yf + int(hf*0.5)), (int(wf*0.5),int(hf*0.5)), 0,0,360,(255, 0, 255), 4)
            # Option pour les lunettes de soleil
            if (activeSunglasses == True):
                point1 = (xf+15,yf+int(0.25*hf))
                point2 = (xf+wf-15,yf+hf-int(0.45*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,sunglasses)
                    webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")
            # Option pour le chapeau
            if (activeHat == True):
                point1 = (xf,yf-int(0.40*hf))
                point2 = (xf+wf,yf+hf-int(0.95*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,hat)
                    webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")

        # Convertir l'image pour Tkinter
        img_tk = convert_image_for_tkinter(webcamImage)

        # Mettre à jour le canevas avec la nouvelle image
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.update()

        if closeWindow == True:
            break

    videoWebcam.release()
    cv.destroyAllWindows()
    canvas.destroy()
    window.destroy()