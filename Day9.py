from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import *

spark = SparkSession \
    .builder \
    .appName("demowordcount-app") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation",True) \
    .config("spark.sql.execution.arrow.pyspark.enabled",True)\
    .config("spark.driver.memory","2g")\
    .config("spark.driver.cores","2")\
    .config("spark.executor.memory","4g")\
    .config("spark.executor.cores","2")\
    .config("spark.sql.streaming.checkpointLocation","c:\\tmp\\logs")\
    .getOrCreate()

#let spark logging level to ERROR to avoid other logs
spark.sparkContext.setLogLevel("ERROR")

try:
    # readStream create a unbounded table and keeps the records adding for ever
    product_ds = spark \
        .readStream \
        .format("rate") \
        .option("rowsPerSecond", 2) \
        .load()
    
    
    print("started streaming..",product_ds.isStreaming)


    prod_df =  product_ds.withColumn("output", col("value") + lit(1))
    
    
    # run the query that prints the counts to console
    #trigger 
    query = prod_df \
        .writeStream \
        .outputMode("append") \
        .option("truncate",False) \
        .trigger(processingTime='2 seconds') \
        .format("console") \
        .start().awaitTermination()

    #query.stop()#stop the streaming

except Exception as ex:
    print("Error occured",ex)
finally:
    spark.stop()









