from keras.models import load_model
import cv2
import numpy as np


def get_prediction(imgName):
    loaded_model = load_model('./model.h5')
    # imgName = 'D:/Jupyter Notebook/plant-seedlings-classification/train/Black-grass/0ace21089.png'
    CLASS = ['Black-grass', 'Charlock', 'Cleavers', 'Common Chickweed',
             'Common wheat', 'Fat Hen', 'Loose Silky-bent', 'Maize',
             'Scentless Mayweed', 'Shepherds Purse',
             'Small-flowered Cranesbill', 'Sugar beet']

    clearTestImg = []
    testImg = []
    testImg.append(cv2.resize(cv2.imread(imgName), (70, 70)))
    testImg = np.asarray(testImg)

    blurImg = cv2.GaussianBlur(testImg[0], (5, 5), 0)
    hsvImg = cv2.cvtColor(blurImg, cv2.COLOR_BGR2HSV)

    lower_green = (25, 40, 50)
    upper_green = (75, 255, 255)
    mask = cv2.inRange(hsvImg, lower_green, upper_green)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    bMask = mask > 0

    clear = np.zeros_like(testImg[0], np.uint8)
    clear[bMask] = testImg[0][bMask]
    clearTestImg.append(clear)
    clearTestImg = np.asarray(clearTestImg)
    clearTestImg = clearTestImg / 255

    pred = loaded_model.predict(clearTestImg)
    predNum = np.argmax(pred, axis=1)
    predStr = CLASS[predNum[0]]

    print(predStr)
    return predStr



# get_prediction('D:/Jupyter Notebook/plant-seedlings-classification/train/Black-grass/0ace21089.png')