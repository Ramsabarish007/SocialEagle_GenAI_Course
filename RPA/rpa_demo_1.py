import pyautogui

import time
# from PIL import Image
import pyscreeze

# print("Welcome to python RPA demo")
# Mouse Operations
# pyautogui.click(766, 329)  # Move the mouse to (100, 100) and click
# time.sleeHello, this is a RPA demo using pyautogui library in python!p(2)  # Wait for 1 second
# # pyautogui.rightClick(100,100)  # Right click at (100, 100)

# # time.sleep(2)  # Wait for 1 second
# # pyautogui.doubleClick(2324,889)  # Double click at (100, 100)
# pyautogui.drag(300, 0, duration=0.5)  # Drag the mouse to the right by 300 pixels over 0.5 seconds
# time.sleep(2)  # Wait for 1 second
# pyautogui.scroll(-3000,x = 1382, y = 232)  # Scroll down 500 "clicks"
# pyautogui.scroll(-3000)
# time.sleep(2)  # Wait for 1 second
# Hello, this is a RPA demo using pyautogui library in python!
# time.sleep(2)  # Wait for 1 second

# x,y = pyautogui.position()  # Get the current mouse position
# print(f"Current mouse position: ({x}, {y})")

# pyautogui.click(x, y)  # Click at the current mouse position

# pyautogui.press("enter", presses=3)

# time.sleep(3)

# Click at the current mouse position
# keyboard operation
# time.sleep(1)  # Wait for 1 second
# pyautogui.write('Hello, this is a RPA demo using pyautogui library in python!', interval=0.05)  # Type with a delay of 0.05 seconds between each character
# # Press Ctrl+C to copy
# pyautogui.hotkey('ctrl', '/')
# Hello, this is a RPA demo using pyautogui library in python!


# ------------------------------------------------------
# Image recognition example
# ------------------------------------------------------

pyautogui.sleep(2)
button_location = pyautogui.locateOnScreen('chat.png', confidence=0.8)
if button_location is not None:
    button_point = pyautogui.center(button_location)
    pyautogui.click(button_point)
    print("Button clicked!")
    
# ============================================
# Other operations
# ============================================

# Take a screenshot
print("Taking screenshot...")
print(pyautogui.size())  # Get the screen size
screenshot = pyautogui.screenshot()   
screenshot.save('screenshot.png')  # Save the screenshot to a file