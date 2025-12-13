import pyautogui
import time

# Increase fail-safe and pause between actions
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.0

def wait_and_click(image, confidence=0.8):
    """Wait for an image to appear and click it."""
    while True:
        pos = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        if pos:
            pyautogui.click(pos)
            return
        time.sleep(0.5)

# 1. Open Browser (Example: Windows search bar)
pyautogui.press("win")
time.sleep(1)
pyautogui.typewrite("chrome")     # Change to firefox/edge/etc.
time.sleep(1)
pyautogui.press("enter")

# 2. Wait for browser to load
time.sleep(3)

# 3. Click the address bar
# wait_and_click("address_bar.png")
pyautogui.click(254, 82) 

# 4. Search for today's football matches
pyautogui.typewrite("football match today top rated player")
pyautogui.press("enter")

# # 5. Wait for results to load
# time.sleep(3)

# # 6. Click the first result
# wait_and_click("first_result.png")

# # 7. Example: update top rated player (replace with your logic)
# # This depends on the interface you want to update.
# # For example, click on a field and type data:
# wait_and_click("update_field.png", confidence=0.7)
# pyautogui.typewrite("Top-rated player: (manually insert or automate scraping here)")

print("Automation complete.")
