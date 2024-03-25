import pyautogui
import pyperclip
import pygetwindow as gw
import time
from bs4 import BeautifulSoup

class GuiUtils:
    __slots__ = "window", "visible_map"
    def __init__(self, window_title="Google Chrome"):
        try:
            # Find the window by its title
            self.window = gw.getWindowsWithTitle(window_title)[0]
            self.window.activate()
            self.visible_map = {"left": self.window.left,
                               "top": self.window.top,
                               "right": self.window.right,
                               "bottom": self.window.bottom}
            print("window activated")
            self.visible_map["left"] += 300
            self.visible_map["top"] += 185
            self.visible_map["right"] -= 300
            self.visible_map["bottom"] -= 100
        except IndexError:
            print(f"No window with the title '{window_title}' found")
        except Exception as e:
            print(f"An error occurred with window: {e}")
 
    def get_map_center(self):
        width = self.visible_map["right"] - self.visible_map["left"]
        height = self.visible_map["bottom"] - self.visible_map["top"] - 37
        return width/2, height/2 
    
    def move_mouse(self, x, y):
        pyautogui.moveTo(self.visible_map["left"] + x, self.visible_map["top"] + y)

    def move_and_click(self, x, y):
        self.move_mouse(x, y)
        pyautogui.click()

    def capture_map_screenshot(self, save_path):
        """
        Captures a screenshot of the selected window and saves it to the specified file path.

        Args:
            save_path (str): The file path where the screenshot will be saved.

        Returns:
            bool: True if the screenshot was captured and saved successfully, False otherwise.
        """
        # Check if the window is found
        if self.window:
            # Get the coordinates of the window
            left, top, right, bottom = self.visible_map.values()
            # Capture a screenshot of the window and save it to the specified file
            pyautogui.screenshot(save_path, region=(left, top, right - left, bottom - top))
            
            print(f"Screenshot of window saved successfully at {save_path}")
            return True
        else:
            print(f"Window with title not found")
            return False
        
    def get_html_content(self):
        pyautogui.hotkey('ctrl', 'shift', 'i')  # Atajo para abrir las herramientas de inspección en Google Chrome
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'a')  # Atajo para abrir las herramientas de inspección en Google Chrome
        pyautogui.hotkey('ctrl', 'c')  # Atajo para abrir las herramientas de inspección en Google Chrome
        # Obtén el contenido HTML del portapapeles
        html_content = pyperclip.paste()
        pyautogui.hotkey('ctrl', 'shift', 'i')  # Atajo para abrir las herramientas de inspección en Google Chrome
        return html_content
    
    def get_stats(self):

        # Encuentra el elemento con la expresión XPath proporcionada
        while True:
            try:
                html_content = self.get_html_content()
                # Parsea el HTML con BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                stats = {}
                stats["topPosition"] = soup.find('span', id='statsText', class_='stats-top-position').text
                stats["cellsEaten"] = soup.find('span', id='statsText', class_='stats-cells-eaten').text
                stats["timeAlive"] = soup.find('span', id='statsText', class_='stats-time-alive').text
                stats["highestMass"] = soup.find('span', id='statsText', class_='stats-highest-mass').text
                stats["foodEaten"] = soup.find('span', id='statsText', class_='stats-food-eaten').text
                break
            except:
                print("error getting stats tryingg in 2s: {e}")
                time.sleep(2)
                pass

        return stats
        


gui = GuiUtils()
x, y = gui.get_map_center()
gui.move_mouse(x, y=y-120)
#print(gui.visible_map.values())
#gui.capture_map_screenshot("current_screenshot.jpg")
#print(gui.get_stats())
