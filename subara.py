from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.subaru.ca/WebPage.aspx?WebSiteID=282&WebPageID=4766'
driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'vehicleItem')))

unique_vehicle_data = set()

with open('subaru.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Car Name', 'Image Link', 'Seating Capacity', 'Price'])

    vehicle_items = driver.find_elements(By.CLASS_NAME, 'vehicleItem')

    for vehicle in vehicle_items:
        image_tag = vehicle.find_element(By.CLASS_NAME, 'vehicle')
        image_link = image_tag.get_attribute('src') if image_tag else None
        
        car_name_tag = vehicle.find_element(By.CLASS_NAME, 'trimBase')
        car_name = car_name_tag.text.strip() if car_name_tag else None
     
        vehicle_data = (car_name, image_link)

        if vehicle_data not in unique_vehicle_data:
            unique_vehicle_data.add(vehicle_data)
            writer.writerow([car_name, image_link])
            print(f'Car Name: {car_name}')
            print(f'Image Link: {image_link}')
driver.quit()
print("Data saved")
