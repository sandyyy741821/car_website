import pymysql
import csv
import os

# Connect to MySQL database using PyMySQL
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="12345678",  # Change this to your MySQL password
)

cur = mydb.cursor()

# Create the database if it doesn't exist
cur.execute("CREATE DATABASE IF NOT EXISTS north_america")
cur.execute("USE north_america")

# Create the table (na_data) with the desired columns
cur.execute("""
CREATE TABLE IF NOT EXISTS na_data (
    file_name VARCHAR(255),
    model_name VARCHAR(255),
    image_url VARCHAR(255),
    type VARCHAR(255),
    engine_type VARCHAR(255)
);
""")

def insert_csv_to_db_from_directory(directory_path):
    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

    # Loop through each CSV file
    for csv_file in csv_files:
        file_path = os.path.join(directory_path, csv_file)
        
        # Remove the '.csv' extension from the file name
        file_name_without_extension = os.path.splitext(csv_file)[0]

        # Open the CSV with different encoding options to handle possible encoding issues
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:  # Try utf-8 encoding first
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header row if present
                rows = list(csvreader)  # Now you can safely read rows after the file is opened
        except UnicodeDecodeError:
            # If utf-8 fails, try using utf-8-sig or ISO-8859-1
            with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header row if present
                rows = list(csvreader)
        except Exception as e:
            print(f"Error opening file {csv_file}: {e}")
            continue
        
        # Check if the CSV has data
        if not rows:
            print(f"CSV file '{csv_file}' is empty or only contains headers.")
            continue

        # Loop through the rows and insert into the database
        for row in rows:
            # Check the length of the row before inserting
            if len(row) < 4:
                print(f"Skipping row with insufficient columns in file '{csv_file}': {row}")
                continue
            
            model_name = row[0]  # Adjust based on the CSV structure
            image_url = row[1]  # Adjust based on the CSV structure
            type_ = row[2] if len(row) > 2 else None  # Set default value if missing
            engine_type = row[3] if len(row) > 3 else None  # Set default value if missing
            
            # Insert data into the na_data table, including the file name (without .csv)
            cur.execute("""
            INSERT INTO na_data (file_name, model_name, image_url, type, engine_type)
            VALUES (%s, %s, %s, %s, %s)
            """, (file_name_without_extension, model_name, image_url, type_, engine_type))

        # Commit changes to the database after each file
        mydb.commit()
        print(f"{len(rows)} rows inserted from file '{csv_file}' into the na_data table.")

# Call the function with the directory path containing your CSV files
insert_csv_to_db_from_directory('na_brands')  # Adjust the directory path if needed

# Check the inserted data
cur.execute("SELECT * FROM na_data")
for row in cur.fetchall():
    print(row)

# Close the database connection
mydb.close()
