import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

# continue with the rest of the code

r_options = Options()
r_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=r_options ,keep_alive=True)
driver.get("https://www.google.com")

finding =  driver.find_element("name", "q")
finding.send_keys("Selenium")
finding.send_keys(Keys.RETURN)

# time.sleep(5)
# wait = WebDriverWait(driver, 10)
# element = wait.until(EC.visibility_of_element_located(("name", "q")))

# Wait for the page to be completely loaded
print(f"{datetime.now()} Wait for page loaded!!!!!!!!!")
WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
print(f"{datetime.now()} Page is ready!!!!!!!!!")

results = driver.find_elements(By.CSS_SELECTOR, 'a[jsname^="UWck"]')
print(f'Number of results: {len(results)}')

for idx, result in enumerate(results):
    print(f'{idx + 1} - {result.text}')
    print(f'Link: {result.get_attribute("href")}')
    
    print("Open the link in a new tab") 
    driver.execute_script("window.open(arguments[0], '_blank')", result.get_attribute("href"))
    
    # Check how many windows are open in the driver
    window_handles = driver.window_handles
    num_windows = len(window_handles)
    print(f"Number of open windows: {num_windows}\n")
    
print(f'Number of open windows: {len(driver.window_handles)}')
print(f'Current window: {driver.current_window_handle}')
print(f'all windows: {driver.window_handles}')


for idx, window in enumerate(window_handles):
    print(f"\nSwitching to window {idx + 1}")
    driver.switch_to.window(window)
    print(f"Title of the window: {driver.title}")
    print(f"URL of the window: {driver.current_url}")
    print("Close the window\n")
    driver.close()
    # print("Switch back to the main window\n")
    # driver.switch_to.window(window_handles[0])

# driver.close()
print('################### Done! ###################')




