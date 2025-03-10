from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument('--headless')  
options.add_argument('--disable-gpu') 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extract_data():
    try:
        driver.get("https://shop.ford.ca/showroom/?pos=kba&lang=en&linktype=build#/") 

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class, 'veh-year-desc-wrap')]"))
        )

        vehicles = driver.find_elements(By.XPATH, "//*[contains(@class, 'veh-year-desc-wrap')]")
        for vehicle in vehicles:
            try:
                year = vehicle.find_element(By.XPATH, ".//span[contains(@class, 'np-year')]").text
                model_name = vehicle.find_element(By.XPATH, ".//strong[contains(@class, 'np-desc')]").text
                print(f"Year: {year}, Model: {model_name}")

                img_url = vehicle.find_element(By.XPATH, ".//following-sibling::div[contains(@class, 'vehicle-img-wrap')]//img").get_attribute('src')
                print("Image URL:", img_url)

                price = vehicle.find_element(By.XPATH, ".//following-sibling::div[contains(@class, 'price-box')]//span[contains(@class, 'dollar-amt')]").text
                print("Price:", price)

            except Exception as e:
                print("Error extracting data for a vehicle:", str(e))

    except Exception as e:
        print("Error:", str(e))

extract_data()

driver.quit()
