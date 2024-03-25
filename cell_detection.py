import cv2
import numpy as np
import math
import time

class CircleDetector:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
    
    def preprocess_image(self):
        # Apply a median filter to reduce noise
        self.smoothed_gray = cv2.medianBlur(self.gray, 23)
        self.smoothed_hsv = cv2.medianBlur(self.hsv, 23)
        
        # Threshold the grayscale image to remove areas close to white
        _, self.thresholded = cv2.threshold(self.smoothed_gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Define the range of yellow color in HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
        
        # Create a mask for the yellow color
        mask_yellow = cv2.inRange(self.smoothed_hsv, lower_yellow, upper_yellow)
        
        # Apply the mask to the grayscale thresholded image
        self.thresholded_yellow = cv2.bitwise_or(self.thresholded, mask_yellow)
    
    def detect_circles(self):
        self.preprocess_image()
        # Detect edges in the image
        edges = cv2.Canny(self.thresholded_yellow, 100, 200)
        
        # Apply Hough Transform for circles
        self.circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=10,
                                         param1=100, param2=20, minRadius=0, maxRadius=0)
        
        if self.circles is not None and len(self.circles):
            self.circles = CircleDetector.remove_by_desnity(self.circles, base_image=self.thresholded_yellow, density_threshold=200)
            self.circles = CircleDetector.remove_overlapping_circles(self.circles)
        return self.circles
    
    def draw_detected_circles(self):
        # Check if circles were found
        if self.circles is not None:
            self.circles = np.uint16(np.around(self.circles))
            for circle in self.circles:
                x, y, r = circle[0], circle[1], circle[2]
                cv2.circle(self.image, (x, y), r, (0, 255, 0), 2)
                cv2.circle(self.image, (x, y), 2, (0, 0, 255), 3)
    
    def display_image(self):
        cv2.imshow('Detected Circles', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def save_image(self, filename):
        cv2.imwrite(filename, self.image) 

    @staticmethod
    def circle_intersection_area(x1, y1, r1, x2, y2, r2):
        """
        Calculates the area of intersection between two circles.

        Args:
            x1, y1 (float): Coordinates of the center of the first circle.
            r1 (float): Radius of the first circle.
            x2, y2 (float): Coordinates of the center of the second circle.
            r2 (float): Radius of the second circle.

        Returns:
            float: Area of intersection between the two circles.
        """
        d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if d >= r1 + r2:
            return 0

        if d <= abs(r1 - r2) and r1 >= r2:
            return math.pi * r2**2
        elif d <= abs(r1 - r2) and r2 > r1:
            return math.pi * r1**2

        a = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
        b = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
        c = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))

        return a + b - c

    @staticmethod
    def circle_intersection_percentage(x1, y1, r1, x2, y2, r2, threshold=0.85):
        """
        Calculates the percentage of intersection between two circles relative to the smaller circle's area.

        Args:
            x1, y1 (float): Coordinates of the center of the first circle.
            r1 (float): Radius of the first circle.
            x2, y2 (float): Coordinates of the center of the second circle.
            r2 (float): Radius of the second circle.
            threshold (float): Threshold for intersection percentage.

        Returns:
            bool: True if the intersection percentage is greater than or equal to the threshold, False otherwise.
        """
        intersection_area = CircleDetector.circle_intersection_area(x1, y1, r1, x2, y2, r2)
        min_circle_area = min(math.pi * r1**2, math.pi * r2**2)
        intersection_percentage = intersection_area / min_circle_area
        return intersection_percentage >= threshold

    @staticmethod
    def remove_overlapping_circles(circles):
        """
        Removes overlapping circles from a list of circles.

        Args:
            circles (list): List of circle parameters (x, y, r).

        Returns:
            list: List of non-overlapping circles.
        """
        deleted_circles = []
        final_circles = []
        del_idx = set()

        for i, circle1 in enumerate(circles):
            x1, y1, r1 = circle1
            x1, y1, r1 = np.float64(x1), np.float64(y1), np.float64(r1)

            if i in del_idx:
                continue
            for j, circle2 in enumerate(circles[i+1:]):
                s2_idx = i+j+1
                if s2_idx in del_idx:
                    continue
                x2, y2, r2 = circle2
                x2, y2, r2 = np.float64(x2), np.float64(y2), np.float64(r2)

                distance = np.sqrt(np.float64((x2 - x1)**2 + (y2 - y1)**2))

                if distance < r1 + r2 and CircleDetector.circle_intersection_percentage(x1, y1, r1, x2, y2, r2, threshold=0.6):
                    del_idx.add(i if r1 < r2 else s2_idx)

        for i, circle in enumerate(circles):
            if i in del_idx:
                deleted_circles.append(circle)
            else:
                final_circles.append(circle)

        return np.array(final_circles)

    @staticmethod
    def remove_by_desnity(circles, base_image, density_threshold):
        density = []
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, r = circle[0], circle[1], circle[2]
            
            # Create a mask for the circle
            mask = np.zeros_like(base_image)
            cv2.circle(mask, (x, y), r, 255, thickness=-1)
            
            # Apply the threshold to the mask
            masked_thresholded = cv2.bitwise_and(base_image, mask)
            
            # Calculate pixel density
            pixel_density = np.sum(masked_thresholded) / (np.pi * r**2)
            if pixel_density > density_threshold:
                density.append((x, y, r))
        return np.array(density)
    
    
if __name__ == "__main__":
    init = time.time()
    detector = CircleDetector('current_screenshot.jpg')
    detector.detect_circles()
    detector.draw_detected_circles()
    #detector.display_image()
    detector.save_image("test-save-2.jpg")
    print(time.time() - init)