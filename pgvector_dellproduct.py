#pip install psycopg2-binary
#pip install timescale_vector

import psycopg2
import numpy as np
from timescale_vector import client
from pgvector.psycopg2 import register_vector

DB_HOST ="cac14mx5xd.ggsugnpmh9.tsdb.cloud.timescale.com"
DB_PORT = "38201"
DB_NAME = "tsdb"
DB_USER = "tsdbadmin"
DB_PASSWORD = "Admin@123456789"

# Function to connect to the TimescaleDB
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

   
    return conn

# Function to create the products table enabled with Vector
def create_products_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE EXTENSION IF NOT EXISTS vector;
    
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name TEXT NOT NULL,
        product_description TEXT,
        product_price INT,
        vector vector(5)
    );
    """)

    register_vector(conn)
    conn.commit()
    cur.close()
    conn.close()

# Function to insert sample Dell product data
def insert_sample_data():
    conn = get_db_connection()
    cur = conn.cursor()
    sample_data = [
        ('Dell XPS 13', '13.3-inch laptop with high performance and stunning display',40000, np.array([0.15, 0.25, 0.35, 0.45, 0.55])),
        ('Dell XPS 15', '15.6-inch laptop with powerful performance and exceptional display',50000, np.array([0.25, 0.35, 0.45, 0.55, 0.65])),
        ('Dell Inspiron 14', '14-inch laptop with essential features and versatile design',30000, np.array([0.35, 0.45, 0.55, 0.65, 0.75])),
        ('Dell Inspiron 15', '15.6-inch laptop with balanced performance and stylish design',80000, np.array([0.45, 0.55, 0.65, 0.75, 0.85])),
        ('Dell Latitude 7400', '14-inch business laptop with advanced security and productivity features',45000, np.array([0.55, 0.65, 0.75, 0.85, 0.95]))
    ]
    insert_query = """
    INSERT INTO products (product_name, product_description, product_price, vector)
    VALUES (%s, %s, %s, %s)
    """
    cur.executemany(insert_query, sample_data)
    conn.commit()
    cur.close()
    conn.close()

# Function to retrieve product details using pgvector
def retrieve_product_details(vector_query, top_k=5):
    conn = get_db_connection()
    cur = conn.cursor()

    # Query to find the top K similar vectors
    query = """
    SELECT product_id, product_name, product_description,product_price,vector
    FROM products
    ORDER BY vector <-> %s
    LIMIT %s;
    """

    cur.execute(query, (vector_query, top_k))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Return the retrieved product details
    return rows

# Sample vector query (replace with the actual vector you want to query)
vector_query = np.array([0.15, 0.25, 0.35, 0.45, 0.55])

# Create table and insert sample Dell product data
create_products_table()
insert_sample_data()


product_details = retrieve_product_details(vector_query)
for detail in product_details:
    print(f"Product ID: {detail[0]}, Name: {detail[1]}, Description: {detail[2]},Price : {detail[3]} Vector: {detail[4]}")
