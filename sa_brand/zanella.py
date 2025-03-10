from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()  

driver.get('https://www.allcarindex.com/brand/argentina/zanella/zity')

wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
image_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='zanella-zity_001.jpg']")))

image_url = image_element.get_attribute("src")

brand_name = "Zanella"

csv_file_path = 'sa_brands/zanella.csv'

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Image"])
    writer.writerow([brand_name, image_url])

driver.quit()

print(f"Data saved to {csv_file_path}")
