import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2

#img = cv2.imread("C:\\Users\\Adil\\Documents\\handwritten_digit_recognition\\res\\4.png")
img = cv2.imread("res\\toRecognise.png")
IMG_SIZE=28

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray image
resized = cv2.resize(gray, (28,28), interpolation=cv2.INTER_AREA) #resize the image

newimg = tf.keras.utils.normalize(resized, axis=1) #normalizing
newimg = np.array(newimg).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

model = keras.models.load_model("model2")

predictions = model.predict(newimg)
print(np.argmax(predictions))