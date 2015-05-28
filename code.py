import cv2 as cv
from numpy import *
import csv

ABS_PATH = "/Users/anton/PycharmProjects/CropImage/photo"

def readImage(imagePath):
	return cv.imread(imagePath, cv.CV_LOAD_IMAGE_GRAYSCALE)

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


data = readCSVFile(ABS_PATH + "/" + "gender.csv")
images = []
for image in data[0]:
	matImg = readImage(image)
	images.append(matImg)
labels = data[1]
testSample = readImage("/Users/anton/PycharmProjects/CropImage/photo/others/3.jpg")

model = cv.createFisherFaceRecognizer()
model.train(array(images), array(labels))
print("Training over")
predictedLabel = model.predict(testSample)
print(predictedLabel)