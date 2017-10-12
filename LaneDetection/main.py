#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from LaneDetector import LaneDetector
import numpy as np



#reading in an image
image = mpimg.imread('test_images/solidWhiteRight.jpg')

#ROI

# get image dimensions and make internal copy
lane_detector = LaneDetector()
lane_detector.set_image(image)

lane_detector.find_lanes()

output = lane_detector.lines_img
#plt.imshow(output, cmap='gray')
plt.imshow(output)
plt.show()

#edge detection

#line detection

#lane detection