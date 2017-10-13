#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from LaneDetector import LaneDetector
import numpy as np
import cv2

def draw_line(img, line, color=[255, 0, 0], thickness=2):
    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]
    cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

def draw_lane(img, lane):
    if lane.left_line:
        draw_line(img, lane.left_line.line_vector, [0,0,200], 3)    
    if lane.right_line:
        draw_line(img, lane.right_line.line_vector, [0,0,200], 3)


#reading video clip
#clip = cv2.VideoCapture('test_videos/solidWhiteRight.mp4')
#clip = cv2.VideoCapture('test_videos/solidYellowLeft.mp4')
clip = cv2.VideoCapture('test_videos/challenge.mp4')

lane_detector = LaneDetector()
lane_detector.quiet()


while(clip.isOpened()):
    ret,frame = clip.read()

    if frame is not None:
        lane_detector.set_image(frame)
        lane_detector.find_lanes()

        overlay = np.zeros_like(frame)
        draw_lane(overlay, lane_detector.lane)

        img = cv2.addWeighted(frame, 1., overlay, 0.9, 0.)

        cv2.imshow('frame',img)

    if cv2.waitKey(1)&0xFF == ord('q'):
        break

clip.release()
cv2.destroyAllWindows()


# get image dimensions and make internal copy
#lane_detector = LaneDetector()
#lane_detector.set_image(image)
#lane_detector.find_lanes()

#output = lane_detector.lanes_img
#plt.imshow(output, cmap='gray')
#plt.imshow(output)
#plt.show()


