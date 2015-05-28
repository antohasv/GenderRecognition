import cv2
import sys
import CropFace

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
eye_cascade = cv2.CascadeClassifier(sys.argv[2])

video_capture = cv2.VideoCapture(0)

isDetect = False
eyes = ()
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

        if len(faces) == 1 and len(eyes):
            print "Face and Eye detected"
            isDetect = True

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if (cv2.waitKey(1) & 0xFF == ord('q')) or isDetect:
        break

image = frame
(ex, ey, ew, eh) = eyes[0]
eye_left = (ex + ew / 2, ey + eh / 2)

(ex, ey, ew, eh) = eyes[1]
eye_right = (ex + ew / 2, ey + eh / 2)

CropFace(image, eye_left, eye_right, offset_pct=(0.3, 0.3), dest_sz=(200, 200)).save("1.jpg")

#Use to capture image on screen
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
