__author__ = 'anton'

import os.path
import csv
import Queue

ABS_PATH = "/Users/anton/OpenCVS/GenderRecognition/image"
FOLDER_NAME_MAIL = "male"
FOLDER_NAME_FEMALE = "female"
SEPARATOR = ";"
DIVIDER = "\n"

class FileIterator:

    def __init__(self, root):
        self.queue = Queue.Queue()
        self.queue.put(root)
        self.root = root
        self.result = []

    def hasNext(self):
        return not self.queue.empty()

    def next(self):
        path = self.queue.get()
        if (os.path.isdir(path)):
            for subFile in os.listdir(path):
                if not subFile.startswith('.'):
                    self.queue.put(path + "/" + subFile)
        else:
            print(path)
            self.result.append(path)

def getListOfFiles(path, label):
    fileItr = FileIterator(path)
    while (fileItr.hasNext()):
        fileItr.next()
    result = fileItr.result
    resultList = []
    for path in result:
        resultList.append([path, label])
    return resultList

def writeToCsvFile(fileName, data):
    myfile = open(fileName, 'wb')
    wr = csv.writer(myfile, delimiter=';')
    for result in data:
        wr.writerow(result)



def main():
    maleList = getListOfFiles(ABS_PATH + "/" + FOLDER_NAME_MAIL, 0)
    femaleList = getListOfFiles(ABS_PATH + "/" + FOLDER_NAME_FEMALE, 1)
    result = maleList + femaleList
    print(result)
    writeToCsvFile(ABS_PATH + "/" + "gender.csv", result)

if __name__ == "__main__":
    main()
