from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Create brands.csv if it doesn't exist
input_file = "brands.csv"
if not os.path.exists(input_file):
    print(f"{input_file} not found. Creating it now...")
    with open(input_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Brand Name"])  # Header row
        writer.writerows([
            ["Toyota"],
            ["BMW"],
            ["Ford"],
            ["Mercedes-Benz"]
        ])
    print(f"{input_file} created. Please add more brand names if needed.")

# Create output directory for scraped data
output_dir = "car_brands"
os.makedirs(output_dir, exist_ok=True)

# Function to scrape data for a specific brand
def scrape_brand(brand_name):
    # Format brand name for URL (replace spaces with hyphens)
    formatted_name = brand_name.lower().replace(" ", "-")
    url = f"https://www.autoevolution.com/cars/{formatted_name}/"
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    try:
        # Check if the brand page exists
        if "404 Error" in driver.title:
            print(f"Brand page not found for: {brand_name}")
            return

        # Locate all models
        models = driver.find_elements(By.XPATH, "//div[@class='models-list']/ul/li")
        if not models:
            print(f"No models found for brand: {brand_name}")
            return

        # Prepare data for CSV
        data = []
        for model in models:
            try:
                model_name = model.find_element(By.TAG_NAME, "h3").text
                model_url = model.find_element(By.TAG_NAME, "a").get_attribute("href")
                model_image = model.find_element(By.TAG_NAME, "img").get_attribute("src")
                data.append([model_name, model_url, model_image])
            except Exception as e:
                print(f"Error processing model for {brand_name}: {e}")

        # Save data to a CSV file
        output_file = os.path.join(output_dir, f"{brand_name}.csv")
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Model Name", "Model URL", "Image URL"])
            writer.writerows(data)
        print(f"Data saved for brand: {brand_name}")

    except Exception as e:
        print(f"Error scraping brand {brand_name}: {e}")

# Read brand names from the CSV file and scrape data
with open(input_file, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        brand_name = row[0].strip()
        if brand_name:  # Ensure the brand name is not empty
            scrape_brand(brand_name)

# Quit Selenium WebDriver
driver.quit()
print("Scraping complete.")
