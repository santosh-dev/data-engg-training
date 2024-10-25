import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler


products = [
    {"product_id": 1, "product_name": "Dell XPS 13", "product_description": "13.3-inch laptop with high performance and stunning display", "product_price": 40000},
    {"product_id": 2, "product_name": "Dell XPS 15", "product_description": "15.6-inch laptop with powerful performance and exceptional display", "product_price": 45000},
   
]

# Extract the features
product_names = [p['product_name'] for p in products]
product_descriptions = [p['product_description'] for p in products]
product_prices = [p['product_price'] for p in products]

# Generate TF-IDF vectors for product_name and product_description
# TF-IDF Vectorization: Converts text data (product_name and product_description) into numerical vectors.

vectorizer = TfidfVectorizer(max_features=2)  # Limiting to 2 features for simplicity
name_vectors = vectorizer.fit_transform(product_names).toarray()
print(name_vectors)
description_vectors = vectorizer.fit_transform(product_descriptions).toarray()
print(description_vectors)

# Normalize the product prices
scaler = MinMaxScaler()
price_vector = scaler.fit_transform(np.array(product_prices).reshape(-1, 1))

# Combine vectors
combined_vectors = []
for i in range(len(products)):
    combined_vector = np.concatenate((name_vectors[i], description_vectors[i], price_vector[i]))
    # Ensure the vector length is 5
    if len(combined_vector) < 5:
        combined_vector = np.pad(combined_vector, (0, 5 - len(combined_vector)), 'constant')
    combined_vectors.append(combined_vector)

# Add the vectors to the products
for i, product in enumerate(products):
    product['vector'] = combined_vectors[i]

# Print the products with vectors
print('Products count',len(products))
print('-------------------------------------')
for product in products:
    print(product)


import psycopg2
from timescale_vector import client
from pgvector.psycopg2 import register_vector

DB_HOST ="cac14mx5xd.ggsugnpmh9.tsdb.cloud.timescale.com"
DB_PORT = "38201"
DB_NAME = "tsdb"
DB_USER = "tsdbadmin"
DB_PASSWORD = "Admin@123456789"

# Database connection
conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    
    )
cur = conn.cursor()
register_vector(conn)

cur.execute("""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS products_vector (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_description TEXT,
    product_price INT,
    vector vector(5)
);
""")

# Insert products into the database
for product in products:
    cur.execute("""
        INSERT INTO products_vector (product_name, product_description, product_price, vector)
        VALUES (%s, %s, %s, %s)
        """, (product['product_name'], product['product_description'], product['product_price'], product['vector'].tolist()))

conn.commit()
cur.close()
conn.close()
