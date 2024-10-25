from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.types import FloatType
import sys

def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def calculatedividend(shareprice):
    return shareprice*0.2

#userfunc = udf(calculateshareprice,FloatType())

#.option("path","supplierdata.csv") \

spark = SparkSession.builder.appName("dell-data-stream") \
    .master("local[*]") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", True) \
    .config("spark.sql.streaming.checkpointLocation", "file:///tmp/spark/checkpoint") \
    .config("spark.sql.shuffle.partitions", 2)\
    .config("spark.streaming.concurrentJobs","3")\
    .getOrCreate()

#userfunction = udf( lambda value : value * 1.2, FloatType())

#product_aggs = products_ds.select( userfunction("salary"))

spark.udf.register("calcdividend",calculatedividend)

scm_schema=StructType([StructField("Supplier_Contact",StringType(),True),
                          StructField("Company",StringType(),True),
                          StructField("Email",StringType(),True),
                          StructField("Share_Price",FloatType(),True),
                          StructField("Date",DateType(),True)
                          ])

df_scm=spark.readStream.format("csv").schema(scm_schema)\
    .option("header",True)\
    .option("maxFilesPerTrigger",1)\
    .option("includeTimestamp",True)\
    .load("inputsource/supplier")\
    #.select("supplier_contact","company","email","share_price")

df_scm.createOrReplaceTempView("supplier")

df_scm_sql=spark.sql("select supplier_contact,company,email,calcdividend(share_price) as dividend  from supplier")

print("Streaming ",df_scm.isStreaming)

print(df_scm.printSchema())

#aggDF = df_scm.groupBy("company").count()

#option("checkpointLocation", checkpointLocation)

result = df_scm_sql.writeStream.format("console")\
        .outputMode("append")\
        .trigger(processingTime='2 seconds') \
        .start().awaitTermination()

"""aggDF
  .writeStream
  .queryName("aggregate_company")    // this query name will be the table name
  .outputMode("complete")
  .format("memory")
  .start()"""

spark.sql("select * from aggregate_company").show()  

#result.stop()
spark.stop()

def writeStreamer(input: DataFrame, checkPointFolder: str, output: str): StreamingQuery = {
  input
    .writeStream
    .format("parquet")
    .option("checkpointLocation", checkPointFolder)
    .option("path", output)
    .outputMode("append")
    .start()
}