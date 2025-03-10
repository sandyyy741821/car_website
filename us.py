from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import re

driver = webdriver.Chrome()
driver.get("https://www.teoalida.com/cardatabase/list-of-cars-in-us/")

p_elements = driver.find_elements(By.TAG_NAME, "p")[2:]

output_dir = "car_brands_data"
os.makedirs(output_dir, exist_ok=True)

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
            
        else:
            continue
        
        full_text = p.text.strip()
        models_text = full_text.replace(brand + ":", "").strip()
        
        model_list = [model.strip() for model in models_text.split(",") if model.strip()]
        
        if not model_list:
            continue
        
        if model_list[0].lower().startswith(brand.lower()):
            model_list[0] = model_list[0].split(":")[-1].strip()
        
        df = pd.DataFrame({
            "Model": model_list
        })
        
        file_name = f"{output_dir}/{brand.replace(' ', '_').replace(':', '').replace('/', '_')}.csv"
        
        df.to_csv(file_name, index=False)
        print(f"Data for {brand} saved to {file_name}")
    
    except Exception as e:
        print(f"Error processing <p> element: {e}")

driver.quit()
