from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

driver = webdriver.Chrome()  
driver.get('https://www.productfrom.com/product/520809-venirauto-centauro-passenger-car')

wait = WebDriverWait(driver, 10) 

product_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.my-12"))).text

image_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.block")))
image_url = image_element.get_attribute("src")

csv_file_path = 'sa_brands/venirauto.csv'


with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Image"])
    writer.writerow([product_name, image_url])


driver.quit()

print("Data saved")
