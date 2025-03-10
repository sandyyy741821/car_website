import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
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

brand_df = pd.DataFrame({"Brand": brand_names})

output_csv = "brand_names.csv"

brand_df.to_csv(output_csv, index=False)

print(f"Brand names saved")
