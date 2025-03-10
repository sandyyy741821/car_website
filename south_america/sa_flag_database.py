import pymysql
import csv

mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="12345678",  
)

cur = mydb.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS south_america")
cur.execute("USE south_america")

cur.execute("""
CREATE TABLE IF NOT EXISTS flags (
    flag_url VARCHAR(255)
);
""")

def insert(csv_filename):
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        csvread = csv.reader(csvfile)
        next(csvread) 
        rows = list(csvread)
        if not rows:
            print("CSV file is empty or only contains headers.")
            return

        for row in rows:
            flag_url = row[1]  
            cur.execute("INSERT INTO flags (flag_url) VALUES (%s)", (flag_url))
        
        mydb.commit()
        print(f"{len(rows)} rows inserted into the logo table.")

insert('flags_south_america.csv')  
cur.execute("SELECT * FROM flags")
for row in cur.fetchall():
    print(row)

mydb.close()
