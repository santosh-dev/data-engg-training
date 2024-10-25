from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

spark = SparkSession \
    .builder \
    .appName("demowordcount-app") \
    .getOrCreate()

try:

    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()


    words = lines.select(
    explode(
        split(lines.value, " ")
    ).alias("word")
    )


    df_wordcounts = words.groupBy("word").count()



    # run the query that prints the counts to console

    query = df_wordcounts \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()

except Exception as ex:
    print("Error occured",ex)
finally:
    spark.stop()


#nc -lk 9999









