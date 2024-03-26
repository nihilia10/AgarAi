import math

class Vector:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def normalize_vector(self, magnitud):
        # Calculate the components of the vector
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        # Calculate the length of the vector
        length = math.sqrt(dx**2 + dy**2)

        # Normalize the vector by dividing each component by the length
        if length != 0:  # Avoid division by zero
            dx_normalized = dx / length * magnitud
            dy_normalized = dy / length * magnitud
        else:
            dx_normalized = 0
            dy_normalized = 0

        return dx_normalized, dy_normalized
