import cv2
import os
import numpy
import time
import window_capture
import computer_vision


##### Changing the working directory to the file's directory
_t_abspath = os.path.abspath(__file__)
_t_dname = os.path.dirname(_t_abspath)
os.chdir(_t_dname)
for var_name in dir():
	if var_name.startswith( '_t_' ):
		del globals()[var_name]
#####


fps_calc = time.time()

#window_capture.WindowCapture.get_window_names()
#exit()

wincap = window_capture.WindowCapture(' GunboundAccs.txt - Bloco de notas')
compvision = computer_vision.ComputerVision('cc_garden_plot.jpg')

while True:
	
	screenshot = wincap.take_screenshot()
	#rectangles = compvision.find_image(screenshot, threshold=0.5)
	#rectangles = compvision.group_search_results(rectangles)
	#points = compvision.get_center_points(rectangles)

	#screenshot = compvision.draw_crosses(screenshot, points)


	cv2.imshow( 'Video input, press ESC to close', screenshot)
	print(f'FPS: {1/(time.time()-fps_calc)}')
	fps_calc = time.time()
	if cv2.waitKey(1) == 27: # Waits 20ms and checks keys press. Break on ESC press
		break

cv2.destroyAllWindows()



