import cv2
import numpy

def draw_lines(img, line_list, thickness=1, color=(0, 255, 0), line_type=cv2.LINE_4):
	for start_x, start_y, end_x, end_y in line_list:
		cv2.line(img, (start_x, start_y), (end_x, end_y), thickness=thickness, color=color, lineType=line_type)
	return img

def divide_image(img, grid=[1, 1]):
	height, width = img.shape[:2]
	horizontal_lines = []
	vertical_lines = []

	if grid[0] > 1:
		line_distance = int(height/grid[0])
		for i in range(1, grid[0]):
			horizontal_lines.append((0, i*line_distance, width, i*line_distance))

	if grid[1] > 1:
		line_distance = int(width/grid[1])
		for i in range(1, grid[1]):
			vertical_lines.append((i*line_distance, 0, i*line_distance, height))

	if grid[0] > 1 and grid[1] > 1:
		return horizontal_lines, vertical_lines
	elif grid[0] > 1 and grid[1] < 2:
		return horizontal_lines
	elif grid[0] < 2 and grid[1] > 1:
		return vertical_lines

class ComputerVision:
	#Properties
	needle = None
	needle_width = 0
	needle_height = 0
	draw_color = (0, 255, 0)
	line_type = None
	marker_type = None


	def __init__(self, needle_path, img_read_type=cv2.IMREAD_UNCHANGED, draw_color=(0, 255, 0)):
		self.needle = cv2.imread(needle_path, img_read_type)
		self.needle_width = self.needle.shape[1]
		self.needle_height = self.needle.shape[0]

		self.draw_color = draw_color
		self.line_type = cv2.LINE_4
		self.marker_type = cv2.MARKER_CROSS



	def find_image(self, haystack, threshold=0.5, search_method=cv2.TM_CCOEFF_NORMED):
		matchTemplate_results = cv2.matchTemplate(haystack, self.needle, search_method)
		filtered_results = numpy.where(matchTemplate_results >= threshold)
		filtered_results = list(zip(*filtered_results[::-1]))

		rectangle_list = []
		for result in filtered_results:
			rectangle = [int(result[0]), int(result[1]), self.needle_width, self.needle_height]
			rectangle_list.append(rectangle)
			rectangle_list.append(rectangle)

		return rectangle_list
	


	def group_search_results(self, rectangle_list, threshold=1, eps=0.5):
		rectangle_list, weight = cv2.groupRectangles(rectList=rectangle_list, groupThreshold=threshold, eps=eps)
		return rectangle_list
	


	def get_center_points(self, rectangle_list):
		points = []
		for (x, y, rect_w, rect_h) in rectangle_list:
			center_x = x + int(rect_w/2)
			center_y = y + int(rect_h/2)
			points.append((center_x, center_y))
		return points



	def draw_rectangles(self, haystack, rectangle_list):
		for (x, y, rect_w, rect_h) in rectangle_list:
			top_left = (x, y)
			bottom_right = (x + rect_w, y + rect_h)
			cv2.rectangle(haystack, top_left, bottom_right, color=self.draw_color, thickness=2)
		return haystack



	def draw_crosses(self, haystack, point_list):
		for (x, y) in point_list:
			cv2.drawMarker(haystack, (x, y), color=self.draw_color, markerType=self.marker_type)
		return haystack
	

