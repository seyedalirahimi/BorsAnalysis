class Point:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return f'{self.x},{self.y}'


