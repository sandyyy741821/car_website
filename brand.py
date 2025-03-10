import os
import pandas as pd

input_dir = "car_brands_data"
output_csv = "brand_names.csv" 
brand_names = [
    os.path.splitext(file)[0].replace('_', ' ').replace('Tesla', 'Tesla-Motors').replace('Ram', 'Ram-Trucks')  # Change "Ram" to "Ram Trucks"
    for file in os.listdir(input_dir)
    if file.endswith('.csv') and "whole story" not in file.lower()
]

brand_df = pd.DataFrame({"Brand": brand_names})
brand_df.to_csv(output_csv, index=False)

print(f"Brand names saved to {output_csv}")
