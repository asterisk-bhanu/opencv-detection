# OpenCV Detection

[colour_det](https://github.com/asterisk-bhanu/opencv-detection/blob/master/colour_det.py): Asks the user for a colour and the filters the video feed to detect objects of only that colour.
The colour can be provided while executing the file in command line itself. If not provided, the program will explicitly ask for a colour to be input.
It displays 3 windows: 
 * Frame: Displays the input video feed.
 * Foreground Mask: Shows the foreground mask that has been subtracted from the feed.
 * Result: Shows the part of the feed displaying the colour mentioned by the user.
 
[shapes_det](https://github.com/asterisk-bhanu/opencv-detection/blob/master/shapes_det.py): Identifies shapes.
Can use any one out of an image, a video and a camera feed to detect shapes.
To input an image or a video, use appropriate flags. Camera feed will be chosen as the input if no flag is invoked.
Use the standard help flag (-h) to view the list of available flags.

[face_detection](https://github.com/asterisk-bhanu/opencv-detection/blob/master/face_detection.py): Uses Haar Cascades to identify faces in a video feed.
Only frontal_face, smile and eyes are being marked in this program.
Official Paper: https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf

[room_occupancy](https://github.com/asterisk-bhanu/opencv-detection/blob/master/room_occupancy.py): Determines occupancy of a room.
Compares the first frame captured with subsequent frames from a camera feed. 
It displays 3 windows:
* Security Feed: Live camera feed.
* Frame Delta: Comparison between first and current frame.
* Threshold Frame: Shows comparison in binary, diluted.

[functions](https://github.com/asterisk-bhanu/opencv-detection/blob/master/functions.py): Contains definitions of functions used in aforementioned programs.

Performance of any program is subjective to lighting conditions and camera quality.
