import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Input CSV file with brand names and the output CSV file for logos
input_csv = "north_america.csv"  # Update this to your CSV file path
output_csv = "logos.csv"

# Read brand names from the input CSV file
def load_brands_from_csv(input_csv):
    brand_names = []
    with open(input_csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            brand_names.append(row[0].strip())  # Assuming the brand name is in the first column
    return brand_names

# Normalize brand names for comparison (lowercase and split into sets)
def normalize_name(name):
    return set(name.lower().split())

# Load the brand names from the CSV file
brand_names = load_brands_from_csv(input_csv)
brand_name_sets = {brand: normalize_name(brand) for brand in brand_names}

# Set up the webdriver for Selenium
driver = webdriver.Chrome()
driver.implicitly_wait(10)

base_url = "https://1000logos.net/car-logos/"

# Initialize a dictionary to store the brand logo data
brand_logo_data = {}

# Iterate through letters of the alphabet to check for logos
for letter in "abcdefghijklmnopqrstuvwxyz":
    url = f"{base_url}?az={letter}"
    driver.get(url)
    
    logo_divs = driver.find_elements(By.CSS_SELECTOR, "div.post-img.small-post-img")
    
    # Iterate through logo divs to find matching logos
    for div in logo_divs:
        try:
            # Extract the brand name and logo URL from the site
            brand_name_on_site = div.find_element(By.TAG_NAME, "a").get_attribute("title").split(" Logo")[0].strip()
            logo_url = div.find_element(By.TAG_NAME, "img").get_attribute("src")
            
            brand_name_set_on_site = normalize_name(brand_name_on_site)
            
            # Compare the brand names
            for local_brand, local_name_set in brand_name_sets.items():
                if local_name_set & brand_name_set_on_site:  # If there's a match
                    brand_logo_data[local_brand] = logo_url
                    print(f"Matched: {local_brand} -> {logo_url}")
                    break
        except Exception as e:
            print(f"Error processing a logo div: {e}")

# Prepare data to save to CSV
output_data = [["Brand", "Logo URL"]]
for brand in brand_names:
    matched_logo = brand_logo_data.get(brand, "Logo URL not found")
    output_data.append([brand, matched_logo])
    print(f"Final Match: {brand} -> {matched_logo}")

# Save the data into a new CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(output_data)

# Quit the Selenium driver
driver.quit()

print("Logo URLs saved to", output_csv)
