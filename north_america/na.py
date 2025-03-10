import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.teoalida.com/cardatabase/list-of-cars-in-us/")

p_elements = driver.find_elements(By.TAG_NAME, "p")[2:]

brand_names = []

def clean_brand_name(brand):
    return re.sub(r"\(.*", "", brand).strip()

scraping_started = False

for p in p_elements:
    try:
        strong_elements = p.find_elements(By.TAG_NAME, "strong")
        if strong_elements:
            brand = strong_elements[0].text.strip()
            brand = clean_brand_name(brand)
            
            if not scraping_started:
                if brand.lower() == "acura":
                    scraping_started = True
                else:
                    continue
            
            if brand not in brand_names:
                brand_names.append(brand)
            
    except Exception as e:
        print(f"Error processing <p> element: {e}")

driver.quit()

scraped_df = pd.DataFrame({"Brand": brand_names})

input_dir = "north_american_brands"

directory_brands = []

for file in os.listdir(input_dir):
    if file.endswith(".csv"):
        file_path = os.path.join(input_dir, file)
        df = pd.read_csv(file_path)
        directory_brands.extend(df['Manufacturer'].dropna().tolist())

all_brands = scraped_df['Brand'].tolist() + directory_brands

combined_df = pd.DataFrame({"Brand": all_brands})

combined_df = combined_df.drop_duplicates(subset=['Brand'], keep='first').sort_values(by='Brand', ascending=True)

combined_df['Brand'] = combined_df['Brand'].str.strip().str.replace('"', '', regex=False).str.replace("'", "", regex=False)

output_csv = "north_america.csv"
combined_df.to_csv(output_csv, index=False)

print("Data saved")
