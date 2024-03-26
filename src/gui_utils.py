import pyautogui
import pyperclip
import pygetwindow as gw
import time

class GuiUtils:
    __slots__ = "window", "visible_map", "window_title"
    def __init__(self, window_title="Google Chrome", corrections= [0, 0, 0, 0]):
        try:
            # Find the window by its title
            self.window_title = window_title
            self.focus_window()
            self.visible_map = {"left": self.window.left,
                               "top": self.window.top,
                               "right": self.window.right,
                               "bottom": self.window.bottom}
            self.visible_map["left"] += corrections[0]
            self.visible_map["top"] += corrections[1]
            self.visible_map["right"] -= corrections[2]
            self.visible_map["bottom"] -= corrections[3]
        except IndexError:
            print(f"No window with the title '{window_title}' found")
        except Exception as e:
            print(f"An error occurred with window: {e}")
 
    def focus_window(self):
        self.window = gw.getWindowsWithTitle(self.window_title)[0]
        self.window.activate()
    def get_map_center(self):
        width = self.visible_map["right"] - self.visible_map["left"]
        height = self.visible_map["bottom"] - self.visible_map["top"] - 37
        return width/2, height/2 
    
    def move_mouse(self, x, y):
        pyautogui.moveTo(self.visible_map["left"] + x, self.visible_map["top"] + y)

    def move_and_click(self, x, y, relative_center=False, base_visible_map=False):
        if base_visible_map:
            x += self.visible_map["left"]
            y += self.visible_map["top"]
            
        self.move_mouse(x, y)
        pyautogui.click()

    def click(self):
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
            
            #print(f"Screenshot of window saved successfully at {save_path}")
            return True
        else:
            print(f"Window with title not found")
            return False
        
    def get_html_content(self):
        self.focus_window()
        time.sleep(1)
        html_content = ''
        pyautogui.hotkey('ctrl', 'shift', 'i')  # Atajo para abrir las herramientas de inspección en Google Chrome
        
        for _ in range(3): #try 3 times
            print(f"getting stats {_+1}")
            time.sleep(10)
            pyautogui.hotkey('ctrl', 'a')  # Atajo para abrir las herramientas de inspección en Google Chrome
            #pyautogui.hotkey('ctrl', 'a')  # Atajo para abrir las herramientas de inspección en Google Chrome
            pyautogui.hotkey('ctrl', 'c')  # Atajo para abrir las herramientas de inspección en Google Chrome
            #pyautogui.hotkey('ctrl', 'c')  # Atajo para abrir las herramientas de inspección en Google Chrome
            # Obtén el contenido HTML del portapapeles
            html_content = pyperclip.paste()
            if html_content != '':
                break
        pyperclip.copy('')  # Esto efectivamente "limpia" el portapapeles
        pyautogui.hotkey('ctrl', 'shift', 'i')  # Atajo para abrir las herramientas de inspección en Google Chrome
        return html_content
    