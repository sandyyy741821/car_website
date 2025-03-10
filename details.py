import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

input_csv = "brand_names.csv"
output_dir = "brand_data"  
base_url = "https://www.autoevolution.com"

os.makedirs(output_dir, exist_ok=True)

brands = pd.read_csv(input_csv)["Brand"]

service = Service("C:\\Users\\user\\Downloads\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

def brand_data(brand_name):
    search_url = f"{base_url}/{brand_name.replace(' ', '-').lower()}/"  
    
    try:
        driver.get(search_url)
        time.sleep(3)  
        
        model_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col2width.bcol-white.fl"))
        )
        
        models = []
        for element in model_elements:
            model_name = element.find_element(By.TAG_NAME, "h4").text.strip()
            
            img_src = element.find_element(By.TAG_NAME, "img").get_attribute("src")
            
            category = element.find_element(By.CSS_SELECTOR, "p.body").text.strip()
            
            engine_type = element.find_element(By.CSS_SELECTOR, "p.eng").text.strip()
            
            models.append({
                "Model": model_name,
                "Image": img_src,
                "Category": category,
                "Engine Type": engine_type
            })
        
        if not models:
            print(f"No models found for {brand_name}.")
        
        output_file = os.path.join(output_dir, f"{brand_name.replace(' ', '_')}.csv")
        pd.DataFrame(models).to_csv(output_file, index=False)
        print("Data saved")
    
    except Exception as e:
        print(f"Error scraping {brand_name}: {e}")

for brand in brands:
    brand_data(brand)

driver.quit()
