#Imports:
import argparse
import datetime
import time
import cv2
import imutils
from functions import *

#CLI arguments parsing:
argp = argparse.ArgumentParser()
argp.add_argument("-v", "--video", help="Path to the video file.")
argp.add_argument("-a", "--min-area", type=int, default=1000, help="Minimum area of object.")
args = vars(argp.parse_args())

#Check for video provided in arguments:
if args.get("video", None) is None:
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)
else:
    cap = cv2.VideoCapture(args["video"])

firstFrame = None

#Start video stream:
while True:
    ret, frame = cap.read()
    raw = frame
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"
	
    #Break stream if no frame captured.
    if ret == False:
        break

    #Resize and convert frame to grayscale and blur for easier calculations.	
    frame = imutils.resize(frame, width=500)	
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21,21), 0) #Smoothen 21x21 pixel regions to filter high frequency noise.
	
    #Store first frame.
    if firstFrame is None:
        firstFrame = blurred
        continue

    #Absolute difference between first frame and current frame.
    frameDelta = cv2.absdiff(firstFrame, blurred)
    thresh = cv2.threshold(frameDelta, 127, 255, cv2.THRESH_BINARY)[1]

    #Dilate threshold frame.
    thresh = cv2.dilate(thresh, None, iterations=2)
    #Find contours on dilated frame.
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    #Loop to show contours.
    for c in cnts:
        if cv2.contourArea(c)<args["min_area"]: #Ignore small area.
            continue
		
        #Draw box.
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)

    img, det, face = face_det(gray, frame)
    if face == True:
        text="Occupied"    
    if det>=2:
        cv2.imwrite("face.jpg", img)
        #Flip frame.
        flip = cv2.flip(img,0)
        #Write the flipped frame.
        out.write(flip)

    #Draw timestamp and text.
    draw_text(frame, text)
    draw_time(raw)

    #Show the frame and record if the user presses a key
    cv2.imshow("Security Feed", raw)
    cv2.imshow("Threshold Frame", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("Facial Capture", img)
    key = cv2.waitKey(1) & 0xFF
 
    #Break loop at 'q'.
    if key == ord("q"):
        break
 
cap.release()
cv2.destroyAllWindows()
