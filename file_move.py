import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load your delivery items CSV data
df = pd.read_csv('delivery_item.csv')

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

# Step 1: Get existing delivery numbers from the DN_delivery table
cur.execute('SELECT delivery_number FROM "DN_delivery";')
existing_delivery_numbers = set(row[0] for row in cur.fetchall())

# Step 2: Filter DataFrame to include only valid delivery numbers
df_filtered = df[df['delivery_number'].isin(existing_delivery_numbers)]

# Check if the filtered DataFrame is empty
if df_filtered.empty:
    print("No valid delivery numbers found for insertion.")
else:
    print(f"Inserting {len(df_filtered)} records into DN_delivery_items.")

    # Prepare your insert query
    insert_query = """
        INSERT INTO "DN_delivery_items"(delivery_number, no_of_unit, description, quantity, per_unit_kg, unit_type) 
        VALUES %s
    """

    # Convert DataFrame rows into a list of tuples
    data = [tuple(row) for row in df_filtered.itertuples(index=False, name=None)]

    # Use execute_values to insert data in bulk
    execute_values(cur, insert_query, data)

# Commit and close the connection
conn.commit()
cur.close()
conn.close()

