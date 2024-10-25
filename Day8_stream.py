from pyspark.sql import SparkSession
 
spark = SparkSession.builder.appName("demo-spark-job").config("spark.sql.streaming.forceDeleteTempCheckpointLocation", True).getOrCreate()

try:

    lines = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()

    print("started streaming..",lines.isStreaming)
 
    lines.writeStream.outputMode("append").format("console").start().awaitTermination()    

except Exception as ex:
    print("Error occured",ex)
finally:
    spark.stop()