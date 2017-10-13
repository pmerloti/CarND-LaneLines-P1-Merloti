import numpy as np

class LineSegment(object):
    """
    Representation of a line segment with helper methods
    to calculate slope, length, etc.
    """

    slope = None
    y_intercept = None
    
    def __init__(self, line_vector):
        """
        initializes given a 4-d vector in the format [x1,y1,x2,y2]
        """
        self.line_vector = line_vector
        #m=(y2-y1)/(x2-x1)
        self.slope = (line_vector[3]-line_vector[1])/(line_vector[2]-line_vector[0])
        self.y_intercept = line_vector[1] - self.slope*line_vector[0]


    @classmethod
    def from_4d_vector(cls, line_vector):
        return cls(line_vector)
    
    @classmethod
    def from_slope_equation(cls, m,b,min_y,max_y):
        """
        initializes given slope, y-intercept and two y values
        """
        x1=(min_y-b)/m
        x2=(max_y-b)/m
        line_vector = [x1,min_y,x2,max_y]
        return cls(line_vector)
    

    def create_lines(line_vectors):
        """
        helper static method that takes a collection of line array from an
        opencv hough transform and maps to a collection of line segments
        """
        lines = []
        for line_vector in line_vectors:
            lines.append(LineSegment(line_vector[0]))
        return lines

    def create_lines(line_vectors):
        """
        helper static method that takes a collection of line array from an
        opencv hough transform and maps to a collection of line segments
        """
        lines = []
        for line_vector in line_vectors:
            lines.append(LineSegment(line_vector[0]))
        return lines


    def slope_ascendant(self):
        #inverted because in pixel space y points down
        return self.slope < 0

    def slope_descendant(self):
        #inverted because in pixel space y points down
        return self.slope > 0

    def slope_degrees(self):
        return np.rad2deg(np.arctan(self.slope) * np.sign(self.slope));

    def length(self):
        p1=self.line_vector[0:2]
        p2=self.line_vector[2:4]
        return np.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)