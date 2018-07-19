#Imports:
import cv2
import imutils
import time
import datetime
import numpy as np


#Class to detect shape.
class shape_det:
	def __init__(self):
		shape = ""

	def check_sq(self, approx):
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w/ float(h)
		shape = "square" if ar>=0.95 and ar<=1.05 else "quadrilateral"
		return shape
	
	def detect(self, c):
		#Approximate perimeter.
		peri = cv2.arcLength(c, True)
		#Approximate polygon.
		approx = cv2.approxPolyDP(c, 0.04*peri, True)	
		
		#Check for circle.
		circ = False
		area=cv2.contourArea(c)
		if ((len(approx)>8) & (len(approx)<23) & (area>20)):
			shape = "circle"
			return shape
		
		#Dictionary to match shape with approximated number of sides.		
		shape_dict = {  3:"triangle",
				4: self.check_sq(approx),
				5: "pentagon"}
		if len(approx) in shape_dict.keys():
			shape = shape_dict[len(approx)]
		else:
			shape = "unidentified"
		
		return shape


#Function to find contours.
def find_cnt(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	#Find contours in the thresholded image.
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	return cnts


#Function to draw centres.
def draw_cent(image,sd=shape_det()):
	cnts = find_cnt(image)
	#Loop over the contours
	for c in cnts:
	#Compute the center of the contours.
		#Init moments.		
		M = cv2.moments(c)
		if M["m00"] != 0:
			cX = int(M["m10"] / M["m00"]*ratio)
			cY = int(M["m01"] / M["m00"]*ratio)
		else:
			cX, cY = 0, 0
		#Draw the center of the shape on the image.	
		cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
		cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	return image


#Function to draw contour.
def draw_cont(image,detection=False):
	cnts = find_cnt(image)
	#Loop over the contours
	for c in cnts:
		shape = ""
		cX = cY = 0
		#Pass on contours with area smaller than 1000.
		if cv2.contourArea(c)<1000:
			continue
		#Check for shape detection.
		if detection:
			#Init moments.		
			M = cv2.moments(c)
			if M["m00"] != 0:
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
			else:
				cX, cY = 0, 0
			sd=shape_det()			
			shape = sd.detect(c)
		#Draw contours.
		cv2.drawContours(image, [c], -1, (0, 0, 255), 2)
		if detection:		
			#Draw labels on contours.		
			cv2.putText(image, shape, (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	return image


#Draw timestamp and text on frame.
def draw_text(frame, text=""):
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

def draw_time(frame):
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

#Init cascades:
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

#Define the codec and create VideoWriter object.
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('face.mp4',fourcc, 20.0, (640,480))

#Function to detect facial features.
def face_det(gray, frame):
    det = False
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        det = True
        cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey), (ex+ew, ey+eh), (0,0,255), 2)
        smile = smile_cascade.detectMultiScale(roi_gray, 1.2, 22)
        for (sx,sy,sw,sh) in smile:
            cv2.rectangle(roi_color,(sx,sy), (sx+sw, sy+sh), (0,255,0), 2)        
    return frame, det
