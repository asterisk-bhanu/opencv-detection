#Imports:
import numpy as np
import cv2
from functions import *

#Start camera feed.
cap = cv2.VideoCapture(0)

#Loop frames from feed.
while 1:
	ret, frame = cap.read()
	gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#Call face detection function.	
	img, faces, face = face_det(gray_scale, frame)
	print(faces)	
	cv2.imshow('Face Detection',img)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

#Clean up.
cap.release()
cv2.destroyAllWindows()
