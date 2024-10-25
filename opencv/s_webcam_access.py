import cv2
import os

webcam = cv2.VideoCapture(0)

if webcam.isOpened():
	rval, frame = webcam.read()
else:
	rval = False

while rval:
	cv2.imshow( 'Webcam', frame)
	rval, frame = webcam.read()
	key = cv2.waitKey(20) # Break on ESC press
	if key == 27:
		break

cv2.destroyWindow('Webcam')
webcam.release()