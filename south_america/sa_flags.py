from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time

chrome_options = Options()
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(options=chrome_options)  

url = "https://en.wikipedia.org/wiki/Flags_of_South_America"
driver.get(url)

time.sleep(3)

links = driver.find_elements(By.XPATH, "//a[contains(@href, 'File:')]//img")

with open('flags_south_america.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Flag URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for link in links:
        try:
            flag_url = link.get_attribute('src')
            
            writer.writerow({'Flag URL': flag_url})
        
        except Exception as e:
            print(f"Error: {e}")
    
driver.quit()

print("Data saved to 'flags_south_america.csv'")
