import pyautogui
import time
import os

def take_screenshot():
    time.sleep(1)  # Delay to allow screen to render
    screenshot = pyautogui.screenshot()
    
    # Your custom folder path
    save_path = r"C:\\Users\\vedan\\OneDrive\\Pictures\\Screenshots 1"

    # Create the folder if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    filename = f"screenshot_{int(time.time())}.png"
    filepath = os.path.join(save_path, filename)

    screenshot.save(filepath)
    return filepath
