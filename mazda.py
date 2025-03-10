import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

chrome_options = Options()
chrome_options.add_argument("--headless")  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.mazda.ca/"  

driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mz-jelly-content'))
)

cars = []

car_elements = driver.find_elements(By.CSS_SELECTOR, 'div.mz-jelly-content')

for car_element in car_elements:
    try:
        name_element = car_element.find_element(By.CSS_SELECTOR, '.h5')
        name = name_element.text.strip() if name_element else None
        
        img_element = car_element.find_element(By.XPATH, '..//following-sibling::div[contains(@class, "mz-image")]//img')
        img_url = img_element.get_attribute('src') if img_element else None

        if img_url:
            full_img_url = urljoin(url, img_url)
        else:
            full_img_url = None
        
        if name and full_img_url:
            cars.append({'name': name, 'image_url': full_img_url})
    except Exception as e:
        print(f"Error extracting data for one car: {e}")

csv_file = "mazda.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'image_url'])
    writer.writeheader()
    writer.writerows(cars)

print(f"Data has been successfully saved to {csv_file}")

driver.quit()
