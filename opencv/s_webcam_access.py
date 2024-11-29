import cv2
import os

webcam = cv2.VideoCapture(0)



if webcam.isOpened():
	rval, frame = webcam.read()
else:
	rval = False

while rval:
	cv2.imshow( 'Webcam, press ESC to close', frame)
	rval, frame = webcam.read()
	frame = cv2.line(frame, (0, 0), (100, 100), (0, 255, 0), 5)
	if cv2.waitKey(20) == 27: # Waits 20ms and checks keys press. Break on ESC press
		break

cv2.destroyWindow('Webcam')
webcam.release()