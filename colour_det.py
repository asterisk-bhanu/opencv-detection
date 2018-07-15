#Imports:
import numpy as np
import cv2


#Video feed initialiser.
video = cv2.VideoCapture(0)


#Frame set.
video.set(3,640)
video.set(4,480)


#Extract foreground mask and background from feed.
fgbg = cv2.createBackgroundSubtractorMOG2()
sensitivity = 30
colour = input("Enter the colour to detect:")
col_dict = {"red": 180,
            "yellow":30,
            "green":60,
            "turquoise":90,
            "blue":120,
           "purple":150,
           }
thresh = col_dict[colour.lower()]


#Display results.
while(1):
    ret, frame = video.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    vid_masked = fgbg.apply(frame)
    
    low = np.array([thresh - sensitivity, 50, 50])
    high = np.array([thresh + sensitivity, 255, 255])
    
    mask = cv2.inRange(hsv, low, high)
    cv2.imshow('Frame', frame)
    
    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Result', result)
    
    cv2.imshow('Foreground Mask', vid_masked)
    
    if cv2.waitKey(30) & 0xff == ord('q'):
        break

#Clean up.
video.release()
cv2.destroyAllWindows()

