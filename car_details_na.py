from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Read brand names from CSV
def read_brands_from_csv():
    brands = []
    with open('official_links.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            first_word = row[0].split()[0]  # Take only the first word of the brand name
            brands.append(first_word)  # Only append the first word of the brand name
    return brands

# Function to search for the brand and scrape car details
def get_car_details(brand_name):
    search_url = f"https://www.autoevolution.com/cars/{brand_name.lower()}/"  # Form the search URL using the brand name
    
    driver.get(search_url)

    # Wait for the page to load completely
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'model-name')]"))
        )
    except Exception as e:
        print(f"Error waiting for the page to load for {brand_name}: {e}")
        return []

    car_details = []
    
    try:
        # XPaths for car details
        car_models = driver.find_elements(By.XPATH, "//h3[contains(@class, 'model-name')]")
        mileages = driver.find_elements(By.XPATH, "//span[contains(@class, 'value') and contains(text(), 'Mileage')]")
        seating_capacities = driver.find_elements(By.XPATH, "//span[contains(@class, 'value') and contains(text(), 'Seating')]")
        images = driver.find_elements(By.XPATH, "//img[contains(@class, 'model-image')]")
        
        for i in range(len(car_models)):
            car_name = car_models[i].text
            mileage = mileages[i].text if i < len(mileages) else "N/A"
            seating = seating_capacities[i].text if i < len(seating_capacities) else "N/A"
            image_url = images[i].get_attribute("src") if i < len(images) else "N/A"
            
            car_details.append([car_name, mileage, seating, image_url])
    
    except Exception as e:
        print(f"Error fetching details for {brand_name}: {e}")
    
    return car_details

# Function to save car details to a CSV file
def save_car_details_to_csv(company_name, car_details):
    with open(f"{company_name}_car_details.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Model", "Mileage", "Seating Capacity", "Image URL"])
        for detail in car_details:
            writer.writerow(detail)
        print(f"Car details for {company_name} saved.")

# Main logic
brands = read_brands_from_csv()

for brand in brands:
    print(f"Scraping details for {brand}...")
    car_details = get_car_details(brand)
    if car_details:
        save_car_details_to_csv(brand, car_details)
    else:
        print(f"No car details found for {brand}.")

driver.quit()
