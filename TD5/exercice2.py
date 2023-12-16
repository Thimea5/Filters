from matplotlib import pyplot as plt
import cv2
import binascii
import numpy as np

#Read image
fond = cv2.imread('./TD5/images/02_background.jpg')
personnage = cv2.imread('./TD5/images/02_personage.png')
masque = cv2.imread('./TD5/images/02_personage_alpha.png')

# Les "Coordonnées" du coin inférieur droit
d0 = fond.shape[0]-personnage.shape[0]
d1 = fond.shape[1]-personnage.shape[1]

#image de fond découpé
crop_img = fond[d0:personnage.shape[0]+d0, d1:personnage.shape[1]+d1]

# Initialiser une image vide pour le résultat
result = np.zeros_like(personnage)

for i in range(0,personnage.shape[0]):
    for j in range(0,personnage.shape[1]):
        alpha_value = masque[i, j] / 255.0  # Normaliser la valeur alpha entre 0 et 1
        result[i, j] = alpha_value * personnage[i, j] + (1 - alpha_value) * crop_img[i, j]

# Incruster l'image dans le fond
fond[d0:personnage.shape[0] + d0, d1:personnage.shape[1] + d1] = result

#Convertion RGB
fondRgb = cv2.cvtColor(fond, cv2.COLOR_BGR2RGB)
#result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

# Résultat
plt.imshow(fondRgb)
plt.title('Image de fond avec la reine/princesse')
plt.show()