from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd

driver = webdriver.Chrome() 

url = 'https://www.auto-data.net/en/felino-brand-219'
driver.get(url)

time.sleep(5)

vehicle_data = []

model_elements = driver.find_elements(By.CLASS_NAME, 'modeli')

for element in model_elements:
    try:
        img_tag = element.find_element(By.TAG_NAME, 'img')
        image_url = img_tag.get_attribute('src')
        
        model_name = element.find_element(By.TAG_NAME, 'strong').text
        
        vehicle_data.append([model_name, image_url])
    except Exception as e:
        print(f"Error while scraping an item: {e}")
        continue

driver.quit()

os.makedirs('na_brands', exist_ok=True)

df = pd.DataFrame(vehicle_data, columns=['Model', 'Image'])

csv_file_path = 'na_brands/felino.csv'
df.to_csv(csv_file_path, index=False)

print("Data saved")
