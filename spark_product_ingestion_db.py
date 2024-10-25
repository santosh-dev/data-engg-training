from pyspark.sql import SparkSession


#.config("spark.jars", "/mnt/e/Spark-Codebase/etl_scm_data_ingestion/mysql-connector-java-8.0.13.jar")\
  # Create SparkSession
spark = SparkSession.builder \
            .appName('delldemoapp') \
            .master("local[*]")\
            .getOrCreate()
            #.config("spark.driver.extraClassPath", "mysql-connector-java-8.0.13.jar") \
  

filename="/home/santosh/dellproducts.csv"
df_products = spark.read.option("header",True).csv(filename)

try:

    df_products.write \
        .format("jdbc") \
        .option("driver","com.mysql.cj.jdbc.Driver") \
        .option("url", "jdbc:mysql://dell-trg-db.clmgaoseov2b.us-east-1.rds.amazonaws.com:3306/dell_demodb?useSSL=false") \
        .option("dbtable", "santosh_products") \
        .option("ssl",False)\
        .option("user", "admin") \
        .option("password", "rootuser") \
        .mode("append")\
        .save()

except Exception as ex:
    print("Some error occured",ex)
finally:
    spark.stop()