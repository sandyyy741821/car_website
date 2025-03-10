from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import re
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Google Images search URL
google_images_url = "https://www.google.com/imghp"

# Output directory where CSV files will be saved
output_dir = "car_brands_data"
os.makedirs(output_dir, exist_ok=True)

# Function to clean brand name (remove country and any extra text)
def clean_brand_name(brand):
    return re.sub(r"\(.*", "", brand).strip()

# Open the target website
driver.get("https://www.teoalida.com/cardatabase/list-of-cars-in-us/")
p_elements = driver.find_elements(By.TAG_NAME, "p")[2:]

# Loop through each <p> element
for p in p_elements:
    try:
        strong_elements = p.find_elements(By.TAG_NAME, "strong")
        if strong_elements:
            # Extract and clean the brand name
            brand = strong_elements[0].text.strip()
            brand = clean_brand_name(brand)
        else:
            continue

        # Full text of the p element (including models)
        full_text = p.text.strip()
        # Remove the brand and colon to get the models part
        models_text = full_text.replace(brand + ":", "").strip()

        # Split models into a list and clean extra spaces
        model_list = [model.strip() for model in models_text.split(",") if model.strip()]

        if not model_list:
            continue

        # Create a list to hold models and their image links
        data = []

        for model in model_list:
            # Search on Google Images
            driver.get(google_images_url)
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(f"{brand} {model} car")
            search_box.send_keys(Keys.RETURN)

            time.sleep(2)  # Wait for results to load

            # Get the first image
            try:
                image_element = driver.find_element(By.CSS_SELECTOR, "img.Q4LuWd")
                image_link = image_element.get_attribute("src")
            except Exception as e:
                print(f"Could not retrieve image for {brand} {model}: {e}")
                image_link = None

            # Append to data
            data.append({"Model": model, "Image Link": image_link})

        # Create a DataFrame with model names and image links
        df = pd.DataFrame(data)

        # Generate the file name based on the brand name
        file_name = f"{output_dir}/{brand.replace(' ', '_').replace(':', '').replace('/', '_')}.csv"

        # Save the DataFrame to a CSV file
        df.to_csv(file_name, index=False)
        print(f"Data for {brand} saved to {file_name}")

    except Exception as e:
        print(f"Error processing <p> element: {e}")

# Quit WebDriver
driver.quit()
