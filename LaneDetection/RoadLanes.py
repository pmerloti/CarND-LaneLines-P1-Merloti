from LineSegment import LineSegment

class RoadLanes(object):
    """
    Represents a highway or road lane, that can be
    constructed from broken line segments from lane marks on the
    left and right side of the lane
    """
    
    left_line = None
    right_line = None
    min_y = max_y = None

    def __init__(self, left_lines, right_lines, min_y, max_y):
        self.min_y = min_y
        self.max_y = max_y
        self.calculate_left_lane(left_lines)
        self.calculate_right_lane(right_lines)

    def calculate_left_lane(self, left_lines):
        if left_lines is not None:
            m,b = self.calculate_average_line(left_lines)
            self.left_line = LineSegment.from_slope_equation(m,b,self.min_y,self.max_y)

    def calculate_right_lane(self, right_lines):
        if right_lines is not None:
            m,b = self.calculate_average_line(right_lines)
            self.right_line = LineSegment.from_slope_equation(m,b,self.min_y,self.max_y)

    def calculate_average_line(self, lines):
        """
        calculated weighted average line from lines.
        longer lines have more weight
        """
        m_acc = b_acc = l_acc = 0
        for line in lines:
            len = line.length()
            m_acc += line.slope * len
            b_acc += line.y_intercept * len
            l_acc += len

        m_avg = m_acc / l_acc
        b_acc = b_acc / l_acc

        return m_avg,b_acc


        