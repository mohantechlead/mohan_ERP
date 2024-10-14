import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load CSV data
df = pd.read_excel('delivery_item2.xlsx')

# Connect to the Heroku PostgreSQL database
conn = psycopg2.connect(
    dbname="danu52bd6b47kp",
    user="ub3o0thg8i7u2n",
    password="p0c4259e445756f86b375b16ee02bfb7cc427b89b03065beb8462f6164e9642ff",
    host="c5flugvup2318r.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
    port="5432"
)

cur = conn.cursor()

insert_query = """
    INSERT INTO "DN_delivery_items"(delivery_number, no_of_unit, description, quantity, per_unit_kg, unit_type) 
    VALUES %s
"""

# Fetch existing delivery numbers
cur.execute('SELECT delivery_number FROM "DN_delivery"')
existing_numbers = {row[0] for row in cur.fetchall()}

# Filter DataFrame to ensure all delivery numbers exist
valid_data = df[df['delivery_number'].isin(existing_numbers)]

# Log the filtered DataFrame
print("Filtered DataFrame:")
print(valid_data)

# Prepare data for insertion
data = [tuple(row) for row in valid_data.itertuples(index=False, name=None)]

# Insert only if valid data exists
try:
    if data:
        execute_values(cur, insert_query, data)
        print(f"Inserted {len(data)} rows into DN_delivery_items.")
    else:
        print("No valid data to insert.")
except Exception as e:
    print(f"An error occurred: {e}")

# Commit and close the connection
conn.commit()
cur.close()
conn.close()