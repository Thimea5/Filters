from matplotlib import pyplot as plt
import cv2
import binascii

#Read image
obj = cv2.imread('./TD5/images/01_object.jpg')
fond = cv2.imread('./TD5/images/01_background.jpg')

#Convert RGB
objGray = cv2.cvtColor(obj, cv2.COLOR_BGR2GRAY)
fondGray = cv2.cvtColor(fond, cv2.COLOR_BGR2GRAY)
nouvelleImage = cv2.cvtColor(fond, cv2.COLOR_BGR2GRAY)

plt.imshow(objGray, cmap='gray', vmin=0, vmax=255)
plt.title('Objet')
plt.show()

plt.imshow(fondGray, cmap='gray', vmin=0, vmax=255)
plt.title('Fond')
plt.show()


#Get access to a pixel
for i in range(0,fondGray.shape[0]):
    for j in range(0,fondGray.shape[1]):

        pixelFond = float(fondGray[i, j])
        pixelObj = float(objGray[i, j])
        nouvelleImage[i, j] = abs(pixelFond-pixelObj)

# == cv2.absdiff() est une variante

plt.imshow(nouvelleImage,cmap='gray', vmin=0, vmax=255)
plt.title('Nouvelle Image')
plt.show()

#Binarisation
seuil = 20
for i in range(0,nouvelleImage.shape[0]):
    for j in range(0,nouvelleImage.shape[1]):
            if (nouvelleImage[i, j]<seuil):
                nouvelleImage[i, j]=0
            else:
                 nouvelleImage[i, j]=255

plt.imshow(nouvelleImage,cmap='gray', vmin=0, vmax=255)
plt.title('Nouvelle Image binarisé')
plt.show()