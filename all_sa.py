import os
import pandas as pd

# Directory containing the CSV files
input_dir = "south_american_brands"  # Change this if needed

# List to hold all the DataFrames
all_data = []

# Loop through all the CSV files in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        # Read the CSV file into a DataFrame
        file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(file_path)
        
        # Add a column with the country name (optional, but can be useful for reference)
        df['Country'] = filename.replace('.csv', '').replace('_', ' ')
        
        # Append the DataFrame to the list
        all_data.append(df)

# Combine all DataFrames into a single DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

# Remove duplicates based on the 'Manufacturer' column
combined_data = combined_data.drop_duplicates(subset=['Manufacturer'], keep='first')

# Save the combined data to a new CSV file
output_file = "combined_south_american_brands.csv"
combined_data.to_csv(output_file, index=False, encoding='utf-8')

print(f"Combined CSV file with unique manufacturers saved as {output_file}")
