from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()  

driver.get('https://en.wikipedia.org/wiki/MAN_Auto-Uzbekistan')

wait = WebDriverWait(driver, 10)

image_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.thumb img")))

brand_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.gallerytext a")))

data = []

image_urls = [img.get_attribute("src") for img in image_elements]

brand_names = [brand.text for brand in brand_elements]

for i in range(min(len(image_urls), len(brand_names))):
    data.append([brand_names[i], image_urls[i]])

csv_file_path = 'sa_brands/MAN_Auto-Uzbekistan.csv'

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand Name", "Image URL"])
    writer.writerows(data)

driver.quit()

print(f"Data saved to {csv_file_path}")
