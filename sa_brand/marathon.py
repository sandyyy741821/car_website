from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()  
driver.get('https://marathoncars.com/')

wait = WebDriverWait(driver, 10)

model_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4.newsflash-title a")))

image_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "figure.newsflash-image img")))

data = []

model_names = [model.text.strip() for model in model_elements]
image_urls = [img.get_attribute("src") for img in image_elements]

for i in range(min(len(model_names), len(image_urls))):
    data.append([model_names[i], image_urls[i]])

csv_file_path = 'sa_brands/marathoncars.csv'

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Model Name", "Image URL"])
    writer.writerows(data)

driver.quit()

print(f"Data saved to {csv_file_path}")
