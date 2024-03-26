#import sys
#from pathlib import Path
## Obtener el directorio actual de mi_script.py
#directorio_actual = Path(__file__).parent
## Obtener el directorio padre común
#directorio_padre = directorio_actual.parent
## Agregar directorio2 al sys.path
#sys.path.append(str(directorio_padre / "src"))

from src.agar import AgarAi
from src.rectangle_detection import RectangleDetector
from src.gui_utils import GuiUtils
import time
import keyboard

class TrainAgents:
    __slots__ = "gui_driver"
    def __init__(self):
        corrections = [570, 0, 0, 0]
        self.gui_driver = GuiUtils(corrections=corrections)

    @staticmethod
    def dump_stats(stats, filename):
        # Save the dictionary to a JSON file
        try:
            with open(filename, 'a+') as json_file:
                json_file.write(f"{','.join(stats.values())}\n")
                print(f"Successfully dumped stats: {stats}")
                return True
        except Exception as e:
            print(f"Error saving stats: {e}")
            return False
    
    def run_agent(self):
        #Setup Agent
        agent = AgarAi()

        #Runntimer
        while agent.alive:
            agent.next_action()            
        
        stats = agent.get_stats()
        TrainAgents.dump_stats(stats, 'data/agent_stats.csv')

    def run_experiments(self, n_experiments=10):

        for _ in range(n_experiments):
            self.restart_world()
            self.run_agent()

    
    def restart_world(self, take_ss=True):
        agent = AgarAi()
        agent.ready_to_play = False
        restarting_ss = 'img/restarting.jpg'
        sleep_time = 1
        possible_pause_video = False
        while not agent.ready_to_play:
            if take_ss:
                self.gui_driver.capture_map_screenshot(restarting_ss)
            detector = RectangleDetector(restarting_ss)

            rectangles = detector.detect_rectangles()
            widest, _ = detector.get_widest_rectangle(rectangles, max_x=600)
            detector.save_image('img/restarting_out.jpg', [_])
            target_corners = [[242, 468], [273, 378]]
            if self.clickable_restart(widest, target_corners):
                sleep_time = 2
                possible_pause_video = False
            rectangles = detector.detect_rectangles(blur=False)
            widest, _ = detector.get_widest_rectangle(rectangles, min_x=1100)
            target_corners = [[1139, 946], [1222, 113]]

            
            if self.clickable_restart(widest, target_corners, clickable_idx=0):
                sleep_time = 2
                possible_pause_video = True 
                 

            time.sleep(1.5)
            agent.update_state()
            if agent.ready_to_play:
                break
            
            if possible_pause_video:
                self.gui_driver.click()
            
            time.sleep(1.5)
            agent.update_state()
            if agent.ready_to_play:
                break
            
            print(f"Aún no puedo jugar sleping {sleep_time}...")
            time.sleep(sleep_time)
            sleep_time += 1
            #No encontró mas clicks
        print("JUGAMOS!")
            
    def clickable_restart(self, widest, target_corners, clickable_idx=None):
        x, y, _, _ = widest
        for ti in target_corners:
            x2, y2 = ti
            if (x-x2)**2 + (y-y2)**2 <= 10:
                if clickable_idx is not None:
                    x2, y2 = target_corners[clickable_idx] #es al que le debería dar click
                self.gui_driver.move_and_click(x2+10, y2+10)
                print(f"encontré un click")
                return True
        return False
            

