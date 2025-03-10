import os
import pandas as pd

input_dir = "south_american_brands" 
all_data = []

for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(file_path)
        
        all_data.append(df)

combined_data = pd.concat(all_data, ignore_index=True)

combined_data = combined_data.drop_duplicates(subset=['Manufacturer'], keep='first')

output_file = "south_america.csv"
combined_data.to_csv(output_file, index=False, encoding='utf-8')

print(f"Combined CSV file with unique manufacturers saved as {output_file}")
