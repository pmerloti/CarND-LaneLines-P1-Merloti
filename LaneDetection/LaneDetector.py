import numpy as np
import cv2
from LineSegment import LineSegment

class LaneDetector(object):
    """
    Given a source image, implements a pipeline of image processing
    operations to detect lane division markings on a typical
    highway scene.

    ## Typical operation:
        1. call set_image and provide an image for image processing pipeline
        2. call one of the pipeline operations. this will trigger all prior
           operations to perform
        3. artifacts (intermediate images) can be invalid if pipeline step has
           not been executed yet

    ## Pipeline:
        image -> roi -> edge detection -> line detection -> lane detection

    """

    image = roi_img = gray_img = blurred_img = edges_img = lines_img = lanes_img = None
    line_segments = None
    h=0
    w=0
    lane_center_x = 0

    #for gaussian blur
    kernel_size = 13

    #limits for lane detection
    line_perspective_deg = 35
    line_perspective_tolerance = 15

    def set_image(self, image):
        """ entry point for image pipeline """
        self.image = image
        self.h = image.shape[0]
        self.w = image.shape[1]
        print("w={},h={}".format(self.w,self.h))

    def smooth(self):
        """ Apply smoothing algorithm """
        #self.set_road_roi(self.margin_left, self.margin_right, self.horizon_height)



        #convert image to grayscale
        self.gray_img = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        # Define a kernel size for Gaussian smoothing / blurring
        # Note: this step is optional as cv2.Canny() applies a 5x5 Gaussian internally
        self.blurred_img = cv2.GaussianBlur(self.gray_img,(self.kernel_size, self.kernel_size), 0)
        
        print("done")

    def find_edges(self, low_threshold=10, high_threshold=50):
        """ creates an edge image """
        self.smooth()
        self.edges_img = cv2.Canny(self.blurred_img, low_threshold, high_threshold)

    def find_lines(self, rho=5, theta=np.pi/180, threshold=15, min_line_len=10, max_line_gap=5):
        """ uses hough transforms to find lines in the image """

        self.find_edges()

        #mask area
        self.mask_road_roi(self.edges_img)

        lines = cv2.HoughLinesP(self.edges_img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

        self.line_segments = LineSegment.create_lines(lines)
        
        self.lines_img = np.copy(self.image)
        self.draw_lines(self.lines_img, self.line_segments)

    def find_lanes(self):
        """
        splits collection of lines found earlier in the processing pipeline into
        left or right lines (based on slope of the line), then uses a weighted average
        stragegy to come up with one lane object
        """
        #run pipeline through here
        self.find_lines()

        #debug image
        self.lanes_img = np.copy(self.image)

        #find left lines
        left_lines = []
        lines_on_the_left = [x for x in self.line_segments if x.slope_ascendant()]
        print("{0} lines on the left".format(len(lines_on_the_left)))
        for left_line in lines_on_the_left:
            within_tolerance = self.line_within_tolerance(left_line,"left")
            if within_tolerance:
                self.draw_line(self.lanes_img, left_line.line_vector, [255,0,0], 1)
                left_lines = left_line
            print("left: slope={0:0.4f} ({1:0.2f} deg), len={2:0.2f}: {3} >> {4}".\
                format(left_line.slope,left_line.slope_degrees(),left_line.length(),left_line.line_vector,\
                within_tolerance))

        #find right lines
        right_lines = []
        lines_on_the_right = [x for x in self.line_segments if x.slope_descendant()]
        print("{0} lines on the right".format(len(lines_on_the_right)))
        for right_line in lines_on_the_right:
            within_tolerance = self.line_within_tolerance(right_line,"right")
            if within_tolerance:
                self.draw_line(self.lanes_img, right_line.line_vector, [0,255,0], 1)
                right_lines = right_line
            print("right: slope={0:0.4f} ({1:0.2f} deg), len={2:0.2f}: {3} XX {4}".\
                format(right_line.slope,right_line.slope_degrees(),right_line.length(),right_line.line_vector,\
                within_tolerance))

        #create model of lane
        self.lane = RoadLane(left_lines, right_lines)
        #self.draw_lane(self.lanes_img, self.lane)


    def line_within_tolerance(self, line_segment, side):
        #does the angle seem ok?
        lower_angle_limit = self.line_perspective_deg-self.line_perspective_tolerance
        upper_angle_limit = self.line_perspective_deg+self.line_perspective_tolerance
        within_angular_tol = lower_angle_limit <= line_segment.slope_degrees() <= upper_angle_limit
        #is it long enough?
        within_len_tol = line_segment.length() > 15
        #is it on the correct side of the lane?
        if side=="left":
            side_ok = line_segment.line_vector[0] < self.lane_center_x
        else:
            side_ok = line_segment.line_vector[2] > self.lane_center_x
        return within_angular_tol and within_len_tol and side_ok

    def mask_road_roi(self, image, margin_left=80, margin_right=37, horizon_height=255):
        """ 
        creates an ROI in the shape of a triangle intended to
        match the target highway that looks like a triangle because
        of camera perspective projection
        """

        #create lines (y=ax+b) that shape the triangular ROI
        #why triangular? that's what typical road lanes disapearing into
        #the horizon look like
        point_left = [margin_left,self.h]
        point_right = [self.w-margin_right,self.h]
        point_horizon = [margin_left+(point_right[0]-margin_left)/2,self.h-horizon_height]
        
        self.lane_center_x = point_left[0] + (point_right[0]-point_left[0])/2

        fit_left = np.polyfit((point_left[0], point_horizon[0]), (point_left[1], point_horizon[1]), 1)
        fit_right = np.polyfit((point_right[0], point_horizon[0]), (point_right[1], point_horizon[1]), 1)
        fit_bottom = np.polyfit((point_left[0], point_right[0]), (point_left[1], point_right[1]), 1)
        print('point left:{0}, point horizon={1}, point right={2}'.format(point_left, point_horizon, point_right))

        # Find the region inside the lines
        XX, YY = np.meshgrid(np.arange(0, self.w), np.arange(0, self.h))
        region_thresholds = \
            (YY > (XX*fit_left[0] + fit_left[1])) & \
            (YY > (XX*fit_right[0] + fit_right[1])) & \
            (YY < (XX*fit_bottom[0] + fit_bottom[1]))

        # Mask region
        image[~region_thresholds] = 0

    def draw_lines(self, img, lines, color=[255, 0, 0], thickness=2):
        for line in lines:
            self.draw_line(img, line.line_vector, color, thickness)

    def draw_line(self, img, line, color=[255, 0, 0], thickness=2):
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(img, (x1, y1), (x2, y2), color, thickness)
