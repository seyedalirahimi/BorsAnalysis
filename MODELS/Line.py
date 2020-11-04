class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __str__(self):
        return f'({self.point1}) - ({self.point2})'

    def __repr__(self):
        return f'({self.point1}) - ({self.point2})'
