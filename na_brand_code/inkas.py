from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3.vehicle-title")))

driver.get("https://inkasarmored.com/armored-vehicles/")

time.sleep(3)

vehicles = driver.find_elements(By.CLASS_NAME, 'cols')

vehicle_data = []

for vehicle in vehicles:
    try:
        name = vehicle.find_element(By.CSS_SELECTOR, "h3.vehicle-title").text
        image_url = vehicle.find_element(By.TAG_NAME, "img").get_attribute("src")

        vehicle_data.append({
            'Model': name,
            'Image': image_url,
        })
    except Exception as e:
        print(f"Error extracting vehicle data: {e}")

if vehicle_data:
    for vehicle in vehicle_data:
        print(f"Name: {vehicle['name']}")
        print(f"Image URL: {vehicle['image_url']}")
        print()
else:
    print("No vehicle data found")

driver.quit()
