import sqlite3
import pandas as pd

# Load the CSV file
csv_file = "medicine_database.csv"

try:
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} medicines from {csv_file}")
except Exception as e:
    print(f"❌ Error loading CSV file: {e}")
    exit()

# Connect to SQLite database
conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

# Create medicines table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        disease TEXT NOT NULL,
        power TEXT NOT NULL
    )
""")
print("✅ Created 'medicines' table (if not exists)")

# Create orders table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        prescription TEXT NOT NULL,
        matched_medicine TEXT,
        status TEXT DEFAULT 'Pending'
    )
""")
print("✅ Created 'orders' table (if not exists)")

# Convert dataframe to a list of tuples for efficient bulk insertion
medicines_data = list(df.itertuples(index=False, name=None))

# Insert data using executemany for performance
try:
    cursor.executemany("""
        INSERT OR IGNORE INTO medicines (name, disease, power) 
        VALUES (?, ?, ?)
    """, medicines_data)
    print(f"✅ Inserted {len(medicines_data)} medicines into database")
except Exception as e:
    print(f"❌ Error inserting data: {e}")

# Save changes and close connection
conn.commit()
conn.close()

print("✅ Database initialized successfully!")
