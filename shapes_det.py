#Imports:
import argparse
import imutils
from functions import *
import cv2
import numpy as np

#CLI arguments parsing:
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False, help="path to the input image")
ap.add_argument("-v", "--video", required=False, help="path to the input video")
args = vars(ap.parse_args())
 
#Check for image provided in arguments:
if args.get("image", None) is not None:
	#Call function from find_cnt.py to find contours.
	img = cv2.imread(args["image"])
	image = draw_cont(img, detection=True)
	#Display contoured image.
	cv2.imshow("Contoured Image", image)
	key = cv2.waitKey(0)
else:
	#Check for video provided in arguments:
	if args.get("video", None) is None:
		cap = cv2.VideoCapture(0)
		time.sleep(2.0)
	else:
		cap = cv2.VideoCapture(args["video"])
	#Start video stream:
	while True:
		ret, frame = cap.read()
		#Call function from find_cnt.py to find contours.
		img = draw_cont(frame, detection= True)
		#Display contoured feed.
		cv2.imshow("Contoured Feed", img)
		key = cv2.waitKey(1) & 0xFF
		#Check for 'q' to exit.
		if key == ord("q"):
			cap.release()
			break
 		
cv2.destroyAllWindows()
