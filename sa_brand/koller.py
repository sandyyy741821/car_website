from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up the driver (e.g., using Chrome)
driver = webdriver.Chrome()

# Open the website
driver.get("https://www.allcarindex.com/brand/argentina/koller")

# Wait for the elements to load
wait = WebDriverWait(driver, 20)

# Get the brand name (Koller)
brand_name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.u-text.u-text-default.u-text-1 font")))
brand_name = brand_name_element.text.strip()

# Get the image URL (you need to extract the 'src' from the img tag)
img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='brands-k/argentina-koller.jpg']")))
img_url = img_element.get_attribute("src")

# Save the data in a dictionary
data = {
    "brand": [brand_name],
    "image_url": [img_url]
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Save to a CSV file
df.to_csv("sa_brands/koller.csv", index=False)

# Close the driver
driver.quit()
