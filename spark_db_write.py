# Imports
from pyspark.sql import SparkSession
# Create SparkSession
spark = SparkSession.builder \
           .appName('delldemoapp') \
           .config("spark.jars", "mysql-connector-j-8.4.0.jar")\
           .config("spark.driver.extraClassPath","mysql-connector-j-8.4.0.jar")\
           .getOrCreate()

columns = ["id", "name","location","product"]

data = [(101, "Foxconn","Chennai","Keyboard"), (173, "Dry Systems","London","SSD"),
    (105, "Harman","Munich","SSD"),(418, "Pers Justin","Chennai","Motherboard")]

df_supplier = spark.sparkContext.parallelize(data).toDF(columns)

df_supplier.write \
  .format("jdbc")\
  .option("url", "jdbc:mysql://dell-demo-db.cjkgc4iwmvlx.us-east-1.rds.amazonaws.com:3306/dell-demo-db") \
  .option("dbtable", "suppliers") \
  .option("user", "admin") \
  .option("password", "Admin123456789") \
  .save()






