#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from LaneDetector import LaneDetector
import numpy as np
#import cv2


#reading in an image
image = mpimg.imread('test_images/solidWhiteRight.jpg')

#ROI

# get image dimensions and make internal copy
lane_detector = LaneDetector()
lane_detector.set_image(image)

margin_left = 85
margin_right = 37
horizon_height = 255
lane_detector.set_road_roi(margin_left, margin_right, horizon_height)

plt.imshow(lane_detector.roi)
plt.show()


#edge detection

#line detection

#lane detection