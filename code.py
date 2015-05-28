import cv2 as cv
from numpy import *
import csv

ABS_PATH = "/Users/anton/OpenCVS/GenderRecognition/image"

def readCSVFile(filePath):
    images = []
    labels = []
    myfile = open(filePath, 'rt')
    try:
        reader = csv.reader(myfile)
        for row in reader:
            val = str(row[0]).split(";")
            images.append(val[0])
            if val[1] not in labels:
                labels.append(int(val[1]))
    finally:
        pass
    return (images, labels)

class GenderRecognizer:

    def __init__(self):
        print("Init")

    def readImage(self, imagePath):
        return cv.imread(imagePath, cv.CV_LOAD_IMAGE_GRAYSCALE)

    def getData(self):
        print("getData")
        data = readCSVFile(ABS_PATH + "/" + "gender.csv")
        images = []
        for image in data[0]:
            matImg = self.readImage(image)
            print(matImg)
            images.append(matImg)
        labels = data[1]
        return(images, labels)

    def trainingModel(self):
        print("training")
        data = self.getData()
        print(data)
        self.model = cv.createFisherFaceRecognizer()
        self.model.train(array(data[0]), array(data[1]))
        print("Training over")

    def getGender(self, imagePath):
        print("getGender")
        testSample = self.readImage(imagePath)
        predictedLabel = self.model.predict(testSample)
        print(predictedLabel)
        return predictedLabel
