#Imports:
import numpy as np
import cv2

#Init cascades:
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

#Function to detect facial features.
def detection(gray, frame):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey), (ex+ew, ey+eh), (0,0,255), 2)
        smile = smile_cascade.detectMultiScale(roi_gray, 1.2, 22)
        for (sx,sy,sw,sh) in smile:
            cv2.rectangle(roi_color,(sx,sy), (sx+sw, sy+sh), (0,255,0), 2)        
    return frame

#Start camera feed.
cap = cv2.VideoCapture(0)

#Loop frames from feed.
while 1:
	ret, frame = cap.read()
	gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	img = detection(gray_scale, frame)	
	cv2.imshow('Face Detection',img)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

#Clean up.
cap.release()
cv2.destroyAllWindows()
