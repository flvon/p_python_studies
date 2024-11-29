import numpy
import win32gui, win32ui, win32con


def get_window_list():
	winlist = []
	def win_recurs(hwnd, ctx):
		if win32gui.IsWindowVisible(hwnd):
			winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
			print(f'hwnd: {hwnd}, name: {win32gui.GetWindowText(hwnd)}')
	win32gui.EnumWindows(win_recurs, winlist)
	return winlist


def get_all_windows_by_name(name):
	winlist = []
	def win_recurs(hwnd, ctx):
		if win32gui.IsWindowVisible(hwnd):
			if  win32gui.GetWindowText(hwnd) == name:
				winlist.append(hwnd)
	win32gui.EnumWindows(win_recurs, winlist)
	return winlist


class WindowCapture:

	# Properties
	width = 0
	height = 0
	hwnd = None


	# Window argument accepts string or int
	def __init__(self, window=None):

#		if window is None:
#			self.hwnd = win32gui.GetDesktopWindow()
#		elif type(window) == int:
#			self.hwnd = win32gui.FindWindow(window, None)
#		else:
#			self.hwnd = win32gui.FindWindow(None, window)
#
#		if not self.hwnd:
#			raise Exception(f'Window not found: {window}')

		self.hwnd = window

		self.get_window_size()



	def get_window_size(self):
		window_coords = win32gui.GetWindowRect(self.hwnd)
		self.width = max(500, window_coords[2] - window_coords[0])
		self.height = max(500, window_coords[3] - window_coords[1])



	def take_screenshot(self, title_bar_size=0, border_size=0, border_type='vertical_and_bottom'):

		self.get_window_size()

		self.width = self.width - 2*border_size
		if border_type == 'vertical_and_bottom':
			self.height = self.height - title_bar_size - border_size
		elif border_type == 'vertical_bars':
			self.height = self.height - title_bar_size

		
		wDC = win32gui.GetWindowDC(self.hwnd)
		dcObj = win32ui.CreateDCFromHandle(wDC)
		cDC = dcObj.CreateCompatibleDC()
		dataBitMap = win32ui.CreateBitmap()
		dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
		cDC.SelectObject(dataBitMap)
		cDC.BitBlt((0, 0), (self.width , self.height) , dcObj, (border_size, title_bar_size), win32con.SRCCOPY)

		signedIntsArray = dataBitMap.GetBitmapBits(True)
		img = numpy.fromstring(signedIntsArray, dtype='uint8')
		img.shape = (self.height, self.width, 4)
		img = img[...,:3]
		img = numpy.ascontiguousarray(img)

		# Free Resources
		dcObj.DeleteDC()
		cDC.DeleteDC()
		win32gui.ReleaseDC(self.hwnd, wDC)
		win32gui.DeleteObject(dataBitMap.GetHandle())

		return img