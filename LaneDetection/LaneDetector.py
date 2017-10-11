import numpy as np

class LaneDetector(object):
    """
    Given a source image, implements a pipeline of image processing
    operations to detect lane division markings on a typical
    highway scene.

    ## Typical operation:
        1. call set_image and provide an image for image processing pipeline
        2. set verbose level (defalt is silence)
        3. call one of the pipeline operations. this will trigger all prior
           operations to perform
        4. artifacts (intermediate images) can be invalid if correct step in
           pipeline not executed

    ## Pipeline:
              
    image -> roi -> edge detection -> line detection -> lane detection

    """

    image = None
    roi = None
    h=0
    w=0

    def set_image(self, image):
        self.image = image
        self.h = image.shape[0]
        self.w = image.shape[1]
        print("w={},h={}".format(self.w,self.h))


    def set_road_roi(self, margin_left, margin_right, horizon_height):
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.horizon_height = horizon_height

        self.roi = np.copy(self.image)

        #create lines (y=ax+b) that shape the triangular ROI
        #why triangular? that's what typical road lanes disapearing into
        #the horizon look like
        point_left = [margin_left,self.h]
        point_right = [self.w-margin_right,self.h]
        point_horizon = [margin_left+(point_right[0]-margin_left)/2,self.h-horizon_height]
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
        self.roi[~region_thresholds] = [0, 0, 0]

