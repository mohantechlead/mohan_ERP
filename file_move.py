import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load CSV data
df = pd.read_excel('driver.xlsx')

# Connect to the Heroku PostgreSQL database
conn = psycopg2.connect(
    dbname="danu52bd6b47kp",
    user="ub3o0thg8i7u2n",
    password="p0c4259e445756f86b375b16ee02bfb7cc427b89b03065beb8462f6164e9642ff",
    host="c5flugvup2318r.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
    port="5432"
)

# Create a cursor
cur = conn.cursor()

insert_query = """
    INSERT INTO "DN_delivery"(delivery_number,	serial_no,	delivery_date,	total_quantity	,truck_number,	driver_name	,recipent_name) 
    VALUES %s
"""

# Prepare data for insertion
# Convert DataFrame rows into a list of tuples
data = [tuple(row) for row in df.itertuples(index=False, name=None)]

# Use execute_values to insert data in bulk
execute_values(cur, insert_query, data)


# Commit and close the connection
conn.commit()
cur.close()
conn.close()
