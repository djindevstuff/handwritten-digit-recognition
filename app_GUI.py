# importing libraries
#pip install pyqt5
#pip install tensorflow
#pip install opencv-python
#pip install numpy
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2
import sys

# window class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Digit Recogniser")

        # setting geometry to main window
        self.setGeometry(100, 100, 500, 500)

        # creating image object
        self.image = QImage(self.size(), QImage.Format_RGB32)

        # making image color to white
        self.image.fill(Qt.black)

        # variables
        # drawing flag
        self.drawing = False
        # default brush size
        self.brushSize = 25
        # default color
        self.brushColor = Qt.white

        # QPoint object to tract the point
        self.lastPoint = QPoint()

        self.uiComponents()

        self.show()

    def uiComponents(self):
        # creating a push button
        reco = QPushButton("Recognise", self)
        # setting geometry of button
        reco.setGeometry(0, 450, 100, 30)
        # adding action to a button
        reco.clicked.connect(self.recognise)

        # creating a push button
        clr = QPushButton("Clear", self)
        # setting geometry of button
        clr.setGeometry(110, 450, 100, 30)
        # adding action to a button
        clr.clicked.connect(self.clear)

        # self.prediction = self.findChild(QLabel, "prediction")
        # self.prediction.setGeometry(200, 450, 50, 30)

        # creating a label
        self.predicted = QLabel(self)
        # setting geometry to the label
        self.predicted.setGeometry(220, 450, 50, 30)
        self.predicted.setFont(QFont("Sanserif", 17))
        self.predicted.setStyleSheet("QLabel"
                                 "{"
                                 "background : white;"
                                 "}")

    # method for checking mouse cicks
    def mousePressEvent(self, event):

        # if left mouse button is pressed
        if event.button() == Qt.LeftButton:
            # make drawing flag true
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.pos()

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
        
        # checking if left button is pressed and drawing flag is true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            
            # creating painter object
            painter = QPainter(self.image)
            
            # set the pen of the painter
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            
            # draw line from the last point of cursor to the current point
            # this will draw only one step
            painter.drawLine(self.lastPoint, event.pos())
            
            # change the last point
            self.lastPoint = event.pos()
            # update
            self.update()

    # method for mouse left button release
    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            # make drawing flag false
            self.drawing = False

    # paint event
    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)
        
        # draw rectangle on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # method for saving canvas
    def recognise(self):
        filePath = "res\\toRecognise.png"
        self.image.save(filePath)

        img = cv2.imread("res\\toRecognise.png")
        IMG_SIZE=28

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray image
        resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA) #resize the image

        newimg = tf.keras.utils.normalize(resized, axis=1) #normalizing
        newimg = np.array(newimg).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

        model = keras.models.load_model("model4")

        predictions = model.predict(newimg)
        #print(np.argmax(predictions))
        self.predicted.setText(str(np.argmax(predictions)))

    # method for clearing every thing on canvas
    def clear(self):
        # make the whole canvas black
        self.image.fill(Qt.black)
        self.predicted.setText("")
        # update
        self.update()


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing the window
window.show()

# start the app
sys.exit(App.exec())
