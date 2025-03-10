from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import os

south_american_countries = [
    'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay',
    'Peru', 'Suriname', 'Uruguay', 'Venezuela'
]

chrome_options = Options()
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome(options=chrome_options)

url = 'https://en.wikipedia.org/wiki/List_of_current_automobile_manufacturers_by_country'
driver.get(url)

time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

country_sections = soup.find_all('div', {'class': 'mw-heading mw-heading3'})

output_dir = "south_american_brands"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for country in south_american_countries:
    for section in country_sections:
        if section.h3 and country in section.h3.get_text():
            country_name = section.h3.get_text().strip()
            
            manufacturers_div = section.find_next('div', {'class': 'div-col'})
            if manufacturers_div:
                manufacturers = [item.get_text().strip() for item in manufacturers_div.find_all('li')]
                
                csv_filename = os.path.join(output_dir, f"{country_name.replace(' ', '_')}.csv")
                with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Manufacturer"])
                    for manufacturer in manufacturers:
                        writer.writerow([manufacturer])
                print(f"Data for {country_name} saved to {csv_filename}")
            else:
                print(f"No manufacturers found for {country_name}.")
            break

driver.quit()

print("Data extraction completed!")
