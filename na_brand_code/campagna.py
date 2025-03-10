from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time
import os

chrome_options = Options()
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome()

url = "https://en.wikipedia.org/wiki/Campagna_Motors"
driver.get(url)

time.sleep(3)

gallery_items = driver.find_elements(By.CSS_SELECTOR, 'ul.gallery.mw-gallery-traditional li.gallerybox')

image_data = []

for item in gallery_items:
    name_element = item.find_element(By.CSS_SELECTOR, 'div.gallerytext')
    car_name = name_element.text.strip()
    
    img_element = item.find_element(By.CSS_SELECTOR, 'img')
    img_url = img_element.get_attribute('src')
    
    image_data.append([car_name, img_url])

output_dir = "na_brands"

csv_filename = os.path.join(output_dir, "campagna.csv")
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Model", "Image"])  
    writer.writerows(image_data)  

driver.quit()

print("Data saved")
