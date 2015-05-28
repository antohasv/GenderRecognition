import cv2
import sys
from CropFace import CropFace
from code import GenderRecognizer
from PIL import Image

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
eye_cascade = cv2.CascadeClassifier(sys.argv[2])

video_capture = cv2.VideoCapture(0)

genderRecognizer = GenderRecognizer()
genderRecognizer.trainingModel()

isDetect = False
eye_left = ()
eye_right = ()
faces = ()
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #Detect eyes
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        if len(faces) == 1 and len(eyes) == 2:
            if eyes[0][0] < eyes[1][0]:
                (ex, ey, ew, eh) = eyes[0]
                eye_left = (x + ex + ew / 2, y + ey + eh / 2)
                (ex, ey, ew, eh) = eyes[1]
                eye_right = (x + ex + ew / 2, y + ey + eh / 2)
            else:
                (ex, ey, ew, eh) = eyes[1]
                eye_left = (x + ex + ew / 2, y + ey + eh / 2)
                (ex, ey, ew, eh) = eyes[0]
                eye_right = (x + ex + ew / 2, y + ey + eh / 2)
            
            print "Face and Eye detected"
            isDetect = True

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if (cv2.waitKey(1) & 0xFF == ord('q')) or isDetect:
        break

cv2.imwrite( "1.jpg", frame)
print(eye_left)
print(eye_right)
image = Image.open("1.jpg")
CropFace(image, eye_left, eye_right, offset_pct=(0.3, 0.3), dest_sz=(200, 200)).save("01.jpg")

if genderRecognizer.getGender("01.jpg")[0] == 0:
    print "Man"
else:
    print "Woman"

#Use to capture image on screen
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
