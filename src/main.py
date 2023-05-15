import cvision

import cv2 as opencv
import numpy as np

# 91.76% accuracy on mnist digits using K Nearest Neighbor
def knearest_digit_ocr():
    img = opencv.imread("imgs/mnist.png")
    img = opencv.cvtColor(img, opencv.COLOR_BGR2GRAY)
    sets = [np.hsplit(row, 100) for row in np.vsplit(img, 50)] # 5000 20x20 images
    sets = np.array(sets)
    training = sets[:, :50].reshape(-1, 400).astype(np.float32)
    testing = sets[:, 50:100].reshape(-1, 400).astype(np.float32)

    k = np.arange(10)
    training_labels = np.repeat(k, 250)[:,np.newaxis]
    testing_labels = training_labels.copy()

    knn = opencv.ml.KNearest_create()
    knn.train(training, opencv.ml.ROW_SAMPLE, training_labels)

    #ret, result, neighbors, dist = knn.findNearest(testing, k=5)
    #matches = result == testing_labels
    #correct = np.count_nonzero(matches)
    #accuracy = correct * 100 / result.size

def main():
    #extractor = cvision.Puzzle("imgs/puzzle.png")
    #extractor.parse_image()
    knearest_digit_ocr()

if __name__ == '__main__':
    main()