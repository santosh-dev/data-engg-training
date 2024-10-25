from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("example").getOrCreate()


data = [("Alice", 34), ("Bob", 45), ("Charlie", 28)]
df = spark.createDataFrame(data, ["name", "age"])


try:
    df.show()
except Exception as e:
    print("Error occurred when using df.show():", e)

print("Printing DataFrame using df.collect():")
for row in df.collect():
    print(row)

# import sys

# print(sys.executable)