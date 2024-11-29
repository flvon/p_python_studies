import cv2
import os
import numpy
import time
import window_capture
import computer_vision
import threading


def main_function(window_capture):
	'''
	For take_screenshot method, it's necessary to feed the border sizes if you want a proper crop
	Title bar and border size may vary:
	Brotato has 11px borders and 39px title bar
	GunBound has 242px borders and 0px title bar in the fake fullscreen mode
	'''
	global stop_threads
	while not stop_threads.is_set():
		try:
			screenshot = window_capture.take_screenshot(border_size=242, border_type='vertical_bars')
			vert_lines = computer_vision.divide_image(screenshot, [1, 6])
			screenshot = computer_vision.draw_lines(screenshot, vert_lines, thickness=3)
			screenshot = cv2.resize(screenshot, (0, 0), fx=0.7, fy=0.7)

			cv2.imshow( str(window_capture.hwnd), screenshot)
			if cv2.waitKey(5) == 27: # Waits 20ms and checks keys press. Break on ESC press
				stop_threads.set()
				cv2.destroyAllWindows()
				break
		except Exception as err:
			print(err)
			stop_threads.set()
			try:
				cv2.destroyAllWindows()
			except:
				print('No windows to destroy')
	


##### Changing the working directory to the file's directory
_t_abspath = os.path.abspath(__file__)
_t_dname = os.path.dirname(_t_abspath)
os.chdir(_t_dname)
for var_name in dir():
	if var_name.startswith( '_t_' ):
		del globals()[var_name]
#####

stop_threads = threading.Event()
winname = 'GunBound'
winlist = window_capture.get_all_windows_by_name(winname)

thread_list = []
for w in winlist:
	wincap = window_capture.WindowCapture(w)
	t = threading.Thread(target=main_function, args=(wincap,), daemon=True)
	t.start()
	thread_list.append(t)


while not stop_threads.is_set():
	key = cv2.waitKey(50)