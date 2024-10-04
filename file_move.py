import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load CSV data
df = pd.read_csv('delivery.csv')

# Clean up the date column by stripping leading/trailing whitespaces
df['delivery_date'] = df['delivery_date'].str.strip()

# Convert 'delivery_date' column to the format expected by PostgreSQL (YYYY-MM-DD)
df['delivery_date'] = pd.to_datetime(df['delivery_date'], dayfirst=True).dt.strftime('%Y-%m-%d')

# Convert 'serial_no_id' to integers in the CSV
# First, handle any non-numeric or missing values by filling with a default or dropping rows
df['serial_no_id'] = pd.to_numeric(df['serial_no_id'], errors='coerce').fillna(0).astype(int)

# Print unique serial_no_id values after conversion
print("Unique serial_no_id values in the CSV after integer conversion:")
print(df['serial_no_id'].unique())

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="danu52bd6b47kp",
    user="ub3o0thg8i7u2n",
    password="p0c4259e445756f86b375b16ee02bfb7cc427b89b03065beb8462f6164e9642ff",
    host="c5flugvup2318r.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
    port="5432"
)

# Create a cursor
cur = conn.cursor()

# Fetch existing serial_no_id values from the orders table and convert to integers
cur.execute("SELECT serial_no FROM orders")
existing_serial_nos = [int(row[0]) for row in cur.fetchall()]  # Convert to integers

print("Existing serial_no_id values in the orders table (as integers):")
print(existing_serial_nos)

# Filter the DataFrame to keep only valid serial_no_id values that exist in the orders table
df = df[df['serial_no_id'].isin(existing_serial_nos)]
print(f"Filtered DataFrame:\n{df}")

# Check if there's any data to insert
if df.empty:
    print("No data to insert.")
else:
    # Prepare data for insertion
    insert_query = """
        INSERT INTO "DN_delivery"(delivery_date, delivery_number, recipient_name, serial_no_id) 
        VALUES %s
    """

    # Convert DataFrame rows into a list of tuples
    data = [tuple(row) for row in df.itertuples(index=False, name=None)]

    # Use execute_values to insert data in bulk
    try:
        execute_values(cur, insert_query, data)
        conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error during insertion: {e}")

# Always close the cursor and connection
cur.close()
conn.close()
