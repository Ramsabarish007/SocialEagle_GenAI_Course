from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/")

# # Navigation commands
# driver.back()
# driver.forward()
# driver.refresh()        
# driver.maximize_window()
# driver.minimize_window()

# # Locating elements
# element_by_id = driver.find_element(By.ID, "element_id")
# element_by_name = driver.find_element(By.NAME, "element_name")
# element_by_class = driver.find_element(By.CLASS_NAME, "element_class")    
element_by_tag = driver.find_element(By.XPATH, '//*[@id="content"]/ul/li[1]/a')

# wait
wait = WebDriverWait(driver, 10) #process will wait for 10 seconds

element = wait.until(EC.presence_of_element_located((By.ID, 'element_id'))) #wait for element to be present

# interracting with elements
element.click()
element.send_keys("Social eagle")
element.clear()

# Screenshots
driver.save_screenshot("screenshot.png")