import sys
import numpy as np
import cv2 as opencv

# Extracting sudoku puzzle from the input image.
class Puzzle():
    def __init__(self, path: str):
        self.img = None
        self.colored_img = None
        self.size = 270
        self.img_path = path

        self.threshold_max = 255
        self.block_size  = 5 # 5x5 threshold pixel neighboring
        self.threshold_c = 5 # substracted from mean pixel value

        self.canny_min = 50
        self.canny_max = 100

        self.hlines = [] # Detected horizantal lines
        self.vlines = [] # Detected vertical lines

    # Load, convert to grayscale, remove color, apply canny edge detection
    def load_image(self):
        self.img = opencv.imread(self.img_path)
        if self.img is None:
            sys.exit(f"Error when loading {self.img_path}")
 
        self.img = opencv.resize(self.img, (self.size, self.size), interpolation = opencv.INTER_AREA)
        self.img = opencv.cvtColor(self.img, opencv.COLOR_BGR2GRAY)
        self.img = opencv.adaptiveThreshold(self.img, self.threshold_max,
                                    opencv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    opencv.THRESH_BINARY,
                                    self.block_size, self.threshold_c)
        self.colored_img = opencv.cvtColor(self.img, opencv.COLOR_GRAY2BGR)
        self.img = opencv.Canny(self.img, self.canny_min, self.canny_max)
 
    # Detect line coordinates using the Hough lines algorithm
    def detect_lines(self):
        min_gap = 10
        detected_lines = opencv.HoughLines(self.img, 1, np.pi/180, 200)

        for line in detected_lines:
            r, theta = line[0]
            m = np.cos(theta)
            b = np.sin(theta)

            x = m * r
            y = b * r
 
            x1 = int(x + self.size * -b)
            y1 = int(y + self.size * m)
            x2 = int(x - self.size * -b)
            y2 = int(y - self.size * m)
            coords = [x1, y1, x2, y2]
 
            if x1 == x2:
                coords[1] = 0
                coords[3] = self.size
                self.vlines.append(coords)
 
            elif y1 == y2 or y1 + 1 == y2:
                coords[0] = 0
                coords[1] = 0  if y1 == 0 else y1 + 1
                coords[2] = self.size if x2 == self.size else x2 + 1
                self.hlines.append(coords)

        # Sort and remove close duplicates
        # Now each list has a length of 9 (9x9)
        self.vlines.sort(key=lambda x: x[0])
        self.hlines.sort(key=lambda x: x[1])

        hlen = len(self.hlines)
        vlen = len(self.vlines)
        self.hlines = [self.hlines[i] for i in range(1, hlen) if self.hlines[i][1] - self.hlines[i - 1][1] > min_gap]
        self.vlines = [self.vlines[i] for i in range(1, vlen) if self.vlines[i][0] - self.vlines[i - 1][0] > min_gap]

    def debug_lines(self):
        print("Horizantal lines: ")
        for hl in self.hlines:
            opencv.line(colored_img, (hl[0], hl[1]), (hl[2], hl[3]), (0, 0, 255), 1)
            print(f"Start: ({hl[0]},{hl[1]}) | End: ({hl[2]}, {hl[3]})") 

        print("\nVertical lines: ")
        for vl in self.vlines:
            opencv.line(colored_img, (vl[0], vl[1]), (vl[2], vl[3]), (255, 0, 0), 1)
            print(f"Start: ({vl[0]},{vl[1]}) | End: ({vl[2]}, {vl[3]})") 

        opencv.imshow("Detected lines", colored_img)

    # Crop sudoku cell from lines and detect the number that populates it
    def detect_numbers(self):
        block = int(self.size / 9) # 9x9 grid

        for y in range(9):
            posy = 0 if y == 0 else self.vlines[y - 1][0]

            for x in range(9):
                posx = 0 if x == 0 else self.hlines[x - 1][1]
                cropped_img = self.colored_img[posy:posy + block, posx:posx + block]

    def parse_image(self):
        self.load_image()
        self.detect_lines()
        self.detect_numbers()

        self.debug_lines()
        opencv.waitKey(0)