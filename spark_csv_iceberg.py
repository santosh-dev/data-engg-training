from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
    .appName("delldemoiceberg") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.4,org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.0,software.amazon.awssdk:bundle:2.17.178,software.amazon.awssdk:url-connection-client:2.17.178')\
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hadoop") \
    .config('spark.sql.catalog.hdfs_catalog.warehouse', 's3a://dellawsbucket/data')\
    .config('spark.sql.catalog.hdfs_catalog.io-impl', 'org.apache.iceberg.aws.s3.S3FileIO')\
    .config('spark.hadoop.fs.s3a.access.key', "AKIA5FTY62UA5WTVVFQC")\
    .config('spark.hadoop.fs.s3a.secret.key', "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")\
    .getOrCreate()
#org.apache.iceberg.nessie.NessieCatalog
#org.apache.iceberg.dell.ecs.EcsCatalog

df = spark.read.format("csv").load("dellsuppliers.csv")
df.createOrReplaceTempView("tempSalesview")

spark.sql("CREATE or REPLACE TABLE weeklysales USING iceberg AS SELECT * FROM tempSalesview")

#spark.sql("""
  #  CREATE TABLE IF NOT EXISTS products (
   #     id bigint, 
    #    productname string
    #)
    #USING iceberg;
#""")

# df.writeTo("weeklysales").using("iceberg").createOrReplace()

df.write.format("iceberg").mode("append").save("weeklysales")