from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("dell-SalesDataAnalytics") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.23") \
    .getOrCreate()


csv_file_path = 'Superstore.csv'
sales_data_df = spark.read.csv(csv_file_path, header=True, inferSchema=True)

# Perform analytics

total_sales = sales_data_df.agg({'sales_amount': 'sum'}).collect()[0][0]
print(f"Total Sales: {total_sales}")


average_sales = sales_data_df.agg({'sales_amount': 'avg'}).collect()[0][0]
print(f"Average Sales: {average_sales}")


sales_by_category = sales_data_df.groupBy('category').agg({'sales_amount': 'sum'})
sales_by_category.show()


sales_by_region = sales_data_df.groupBy('region').agg({'sales_amount': 'sum'})
sales_by_region.show()

# Database connection parameters
db_url = "jdbc:postgresql://ep-billowing-pond-a450qgrv.us-east-1.aws.neon.tech:5432/demoDB"
db_properties = {
    "user": "demoDB_owner",
    "password": "Pv4lxD3yuWJI",
    "driver": "org.postgresql.Driver"
}

# Write the DataFrame to PostgreSQL
sales_data_df.write.jdbc(url=db_url, table="sales_data", mode="overwrite", properties=db_properties)

print("Data inserted into PostgreSQL successfully.")
