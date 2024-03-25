import random
import math
import time
import json
from gui_utils import GuiUtils
from cell_detection import CircleDetector


class AgarAi:
    __slots__ = "gui_driver", "center_x", "center_y", "objects", "stats"
    def __init__(self):

        try:
            self.gui_driver = GuiUtils()
            self.center_x, self.center_y = self.gui_driver.get_map_center()
            self.objects = []
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def move_to_center(self, x=0, y=0):
        random_x = self.center_x + x
        random_y = self.center_y + y
        # Move the mouse cursor to the random position within the window
        self.gui_driver.move_mouse(random_x, random_y)
    
    def revive(self):
        
        self.gui_driver.move_and_click(self.center_x, y=self.center_y-30)
        time.sleep(20)
        self.gui_driver.move_and_click(self.center_x, y=self.center_y-125)
    
    def move_random(self, time_lapse=10):
        """
        Moves the mouse cursor with a random angle (between 0 and 360) with a radius of 20px from the center of the window 

        Args:
        time_lapse: (int) the time between random cursor changes

        Returns:
        bool: True if the mouse was successfully moved,
              False otherwise
        """
        try:
            while True:
                # Calculate random angle between 0 and 360 degrees
                angle = random.uniform(0, 2*math.pi)

                # Calculate random coordinates within a radius of 20px from the center of the window
                
                radius = 80
                random_x = self.center_x + radius * math.cos(angle)
                random_y = self.center_y + radius * math.sin(angle)

                # Move the mouse cursor to the random position within the window
                self.gui_driver.move_mouse(random_x, random_y)

                # Wait for the specified time before the next movement
                time.sleep(time_lapse)
                self.update_state()
                if not self.im_alive():
                    break
                
            

        except Exception as e:
            print(f"An error occurred: {e}")
            self.dump_stats()
            return False
        
    def update_state(self):
        init = time.time()
        ss_path = 'current_screenshot.jpg'
        self.gui_driver.capture_map_screenshot(ss_path)
        detector = CircleDetector(ss_path)
        self.objects = detector.detect_circles()
        detector.draw_detected_circles()
        detector.save_image("test-save.jpg")
        print(f"{time.time() - init}s updating state")

    def im_alive(self):
        count_rare = 0
        for i in self.objects:
            x, y, r = i
            if (r >= 40 and r <= 50) and (x >= 500 and x <= 800) and (y >= 300 and y <=350):
                count_rare += 1
        if count_rare >= 3:
            self.dump_stats()
            return False
        return True
    
    def dump_stats(self):
        self.stats = self.gui_driver.get_stats()
        # Save the dictionary to a JSON file
        with open('agent_stats.csv', 'a+') as json_file:
            json_file.write(f"{','.join(self.stats.values())}\n")
        return False




