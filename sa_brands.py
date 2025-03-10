from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import os

# South American countries list
south_american_countries = [
    'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay',
    'Peru', 'Suriname', 'Uruguay', 'Venezuela'
]

# Set up the Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for better performance
driver = webdriver.Chrome(options=chrome_options)

# Open the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_current_automobile_manufacturers_by_country'
driver.get(url)

# Wait for the page to load
time.sleep(3)

# Extract page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all country sections with the class "mw-heading mw-heading3"
country_sections = soup.find_all('div', {'class': 'mw-heading mw-heading3'})

# Create directory to store country CSV files
output_dir = "south_american_brands"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each country in the South American list
for country in south_american_countries:
    # Look for the country in the page's sections
    for section in country_sections:
        if section.h3 and country in section.h3.get_text():
            # Country found, now extract the manufacturers
            country_name = section.h3.get_text().strip()
            
            # Find the <div class="div-col"> containing the manufacturers for the country
            manufacturers_div = section.find_next('div', {'class': 'div-col'})
            if manufacturers_div:
                manufacturers = [item.get_text().strip() for item in manufacturers_div.find_all('li')]
                
                # Write data to a CSV file for that country
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

# Close the browser
driver.quit()

print("Data extraction completed!")
