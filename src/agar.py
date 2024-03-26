import random
import math
import time
from src.gui_utils import GuiUtils
from src.cell_detection import CircleDetector
from src.rectangle_detection import RectangleDetector
from bs4 import BeautifulSoup
import random

class AgarAi:
    __slots__ = "gui_driver", "center_x", "center_y", "objects", "alive", "t", "cell_detector", "ss_state", "ready_to_play"
    def __init__(self):

        try:
            corrections = [300,185,300,100]
            self.ss_state = "img/current_screenshot.jpg"
            self.gui_driver = GuiUtils(corrections=corrections)
            self.cell_detector = CircleDetector(self.ss_state)
            self.center_x, self.center_y = self.gui_driver.get_map_center()
            self.objects = []
            self.ready_to_play = True
            self.alive = True
            self.t = 0
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
    
    def move_random(self, radius=80):
        """
        Moves the mouse cursor with a random angle (between 0 and 360) with a radius of 20px from the center of the window 

        Args:
        time_lapse: (int) the time between random cursor changes

        Returns:
        bool: True if the mouse was successfully moved,
              False otherwise
        """
        try:
            # Calculate random angle between 0 and 360 degrees
            angle = random.uniform(0, 2*math.pi)

            # Calculate random coordinates within a radius of 20px from the center of the window

            random_x = self.center_x + radius * math.cos(angle)
            random_y = self.center_y + radius * math.sin(angle)

            # Move the mouse cursor to the random position within the window
            self.gui_driver.move_mouse(random_x, random_y)               
            

        except Exception as e:
            print(f"An error occurred moving random: {e}")
            return False
        
    def update_state(self):
        init = time.time()
        self.t += 1
        print(f"time: {self.t}")

        if self.gui_driver.capture_map_screenshot(self.ss_state):

            #Capture Circle Objects
            self.cell_detector.detect_circles()

            #Capture Boxes
            box_detector = RectangleDetector(self.ss_state)
            rects = box_detector.detect_rectangles() 
            next_button = box_detector.get_widest_rectangle(rects)       

            self.ready_to_play = self.im_ready_to_play()
            self.alive = self.im_alive(next_button)
            total_time = time.time() - init
            with open('data/time_stats.csv', 'a+') as time_file:
                time_file.write(f"{total_time}\n")
                return True
        else:
            print("ERROR: couldnt view map")

    def im_alive(self, next_button):
        un_bound, _ = next_button
        x, y, w, h = un_bound
        if (x >= 500 and x <= 800) and (y >= 280 and y<=300) and w >= 290 and h >= 30:
            print("IM DEAAAAD")
            return False
        return True
    
    def im_ready_to_play(self):
        self.cell_detector.detect_circles(draw=True)
        return self.cell_detector.detect_circle_position(self.center_x, self.center_y)
    
    def get_stats(self):
        sleep_time = 3
        # Encuentra el elemento con la expresión XPath proporcionada
        try:                
            html_content = self.gui_driver.get_html_content()
            # Parsea el HTML con BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            stats = {}
            stats["topPosition"] = soup.find('span', id='statsText', class_='stats-top-position')
            stats["cellsEaten"] = soup.find('span', id='statsText', class_='stats-cells-eaten')
            stats["timeAlive"] = soup.find('span', id='statsText', class_='stats-time-alive')
            stats["highestMass"] = soup.find('span', id='statsText', class_='stats-highest-mass')
            stats["foodEaten"] = soup.find('span', id='statsText', class_='stats-food-eaten')


            assert stats["topPosition"] is not None, "topPosition is None"
            assert stats["cellsEaten"] is not None, "cellsEaten is None"
            assert stats["timeAlive"] is not None, "timeAlive is None"
            assert stats["highestMass"] is not None, "highestMass is None"
            assert stats["foodEaten"] is not None, "foodEaten is None"

            stats["topPosition"] = stats["topPosition"].text
            stats["cellsEaten"] = stats["cellsEaten"].text
            stats["timeAlive"] = stats["timeAlive"].text
            stats["highestMass"] = stats["highestMass"].text
            stats["foodEaten"] = stats["foodEaten"].text
        except Exception as e:
            print(f"error getting stats trying in {sleep_time}s: {e}")
            id = random.randint(0, 1000)
            self.gui_driver.capture_map_screenshot(f'img/stats/{id}_stats.png')
            pass

        return stats
        
    def next_action(self):
        #policy
        radius = 40 + self.t
        self.move_random(radius)
        self.update_state()
